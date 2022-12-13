from eth_event import get_log_topic
from eth_utils import decode_hex
from eth_abi import decode_abi
from typing import List, Dict
import re


def extract_params(abi_params: List[dict]) -> List[str]:
    """
    Returns a list of the types of the parameters for a single
    ABI item.

    :param abi_params: The ABI parameters.
    :return: The list of types.
    """

    types = []
    pattern = re.compile(r'tuple(\[(\d*)\])?')

    # iterate over ABI parameters
    for param in abi_params:
        tuple_match = pattern.match(param['type'])
        if not tuple_match: types.append(param['type'])
        else:
            array, size = tuple_match.group(1, 2)
            tuple_type_tail = f'[{size}]' if array is not None else ''
            types.append(f"({','.join(x for x in extract_params(param['components']))}){tuple_type_tail}")
            continue

    return types


def build_function_map(abi: List[dict]) -> Dict[str, dict]:
    """
    Builds a dictionary that maps function selectors to the 
    function name and parameter types.

    :param abi: The ABI.
    :return: The function map.
    """

    function_map = {}
    for item in abi:
        if 'type' not in item or item['type'] != 'function': continue
        elif 'name' not in item: continue
        function_map[get_log_topic(item)[:10]] = {
            'name': item['name'],
            'inputs': {
                'params': extract_params(item['inputs']),
                'abi': item['inputs']
            },
            'outputs': {
                'params': extract_params(item['outputs']),
                'abi': item['outputs']
            }
        }

    return function_map


def build_topic_map(abi: List[dict]) -> Dict[str, dict]:
    """
    Builds a dictionary that maps event topics to the event name
    and parameter types.

    :param abi: The ABI.
    :return: The topic map.
    """

    topic_map = {}
    for item in abi:
        if 'type' not in item or item['type'] != 'event': continue
        elif 'name' not in item: continue
        topic_map[get_log_topic(item)] = {
            'name': item['name'],
            'params': extract_params(item['inputs']),
            'inputs': item['inputs']
        }

    return topic_map


def decode_hex_data(params: List[str], hex_data: str) -> tuple:
    """
    Decodes the data hex string into a tuple of the parameters.

    :param params: The list of parameter types.
    :param data: The data hex string.
    :return: The decoded tuple.
    """

    data = decode_hex(hex_data)
    decoded_data = decode_abi(params, data)
    return decoded_data


def resolve_decoded_data(decoded_data: tuple, abi_params: List[dict]) -> dict:
    """
    Resolve the decoded data tuple from an eth_abi.decode_abi call
    and the ABI parameters to a dictionary of the parameter names and
    values.

    :param decoded_data: The decoded data tuple.
    :param abi_params: The ABI parameters.
    :return: The dictionary of parameter names and values.
    """

    decoded_params = {}
    for decoded_item, abi_item in zip(decoded_data, abi_params):
        if abi_item['type'] == 'tuple': 
            decoded_tuple_params = resolve_decoded_data(decoded_item, abi_item['components'])
            decoded_params[abi_item['name']] = decoded_tuple_params
        elif abi_item['type'] == 'tuple[]': 
            decoded_tuple_array_params = [resolve_decoded_data(i, abi_item['components']) for i in decoded_item]
            decoded_params[abi_item['name']] = decoded_tuple_array_params
        elif abi_item['type'].endswith('[][]'):
            raise NotImplementedError('Nested arrays are not supported')
        elif abi_item['type'].endswith('[]'):
            decoded_params[abi_item['name']] = list(decoded_item)
        else:
            decoded_params[abi_item['name']] = decoded_item

    return decoded_params