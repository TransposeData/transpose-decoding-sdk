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
    function name, types, and params.

    :param abi: The ABI.
    :return: The function map.
    """

    function_map = {}
    for item in abi:
        if 'type' not in item or item['type'] != 'function': continue
        elif 'name' not in item: continue
        function_map[get_log_topic(item)[:10]] = {
            'name': item['name'],
            'input_order': [i['name'] for i in item['inputs']],
            'output_order': [i['name'] for i in item['outputs']],
            'inputs': {
                'types': extract_params(item['inputs']),
                'params': item['inputs']
            },
            'outputs': {
                'types': extract_params(item['outputs']),
                'params': item['outputs']
            }
        }

    return function_map


def build_topic_map(abi: List[dict]) -> Dict[str, dict]:
    """
    Builds a dictionary that maps event topics to the event name,
    types, and params.

    :param abi: The ABI.
    :return: The topic map.
    """

    topic_map = {}
    for item in abi:
        if 'type' not in item or item['type'] != 'event': continue
        elif 'name' not in item: continue
        topic_map[get_log_topic(item)] = {
            'name': item['name'],
            'order': [i['name'] for i in item['inputs']],
            'topics': {
                'types': extract_params([i for i in item['inputs'] if i['indexed']]),
                'params': [i for i in item['inputs'] if i['indexed']]
            },
            'data': {
                'types': extract_params([i for i in item['inputs'] if not i['indexed']]),
                'params': [i for i in item['inputs'] if not i['indexed']]
            }
        }

    return topic_map


def decode_hex_data(types: List[str], hex_data: str) -> tuple:
    """
    Decodes the data hex string into a tuple of the parameters.

    :param types: The list of parameter types.
    :param data: The data hex string.
    :return: The decoded tuple.
    """

    if hex_data is None: return tuple()
    data = decode_hex(hex_data)
    decoded_data = decode_abi(types, data)
    return decoded_data


def resolve_decoded_data(abi_params: List[dict], decoded_data: tuple) -> dict:
    """
    Resolve the decoded data tuple from an eth_abi.decode_abi call
    and the ABI parameters to a dictionary of the parameter names and
    values.

    :param abi_params: The ABI parameters.
    :param decoded_data: The decoded data tuple.
    :return: The dictionary of parameter names and values.
    """

    # enforce that the number of params matches the number of decoded items
    if len(abi_params) != len(decoded_data):
        raise ValueError('Length of decoded items does not match the number of ABI parameters')

    # recursively resolve the params and decoded items
    decoded_params = {}
    for abi_item, decoded_item in zip(abi_params, decoded_data):
        if abi_item['type'] == 'tuple': 
            decoded_tuple_params = resolve_decoded_data(abi_item['components'], decoded_item)
            decoded_params[abi_item['name']] = decoded_tuple_params
        elif abi_item['type'] == 'tuple[]': 
            decoded_tuple_array_params = [resolve_decoded_data(abi_item['components'], i) for i in decoded_item]
            decoded_params[abi_item['name']] = decoded_tuple_array_params
        elif abi_item['type'].endswith('[][]'):
            raise NotImplementedError('Nested arrays are not supported')
        elif abi_item['type'].endswith('[]'):
            decoded_params[abi_item['name']] = list(decoded_item)
        else:
            decoded_params[abi_item['name']] = decoded_item

    return decoded_params