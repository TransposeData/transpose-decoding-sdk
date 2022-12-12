from eth_event import get_log_topic
from typing import List, Dict
import re


def list_params(abi_params: List[dict]) -> List[str]:
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
            types.append(f"({','.join(x for x in list_params(param['components']))}){tuple_type_tail}")
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
            'params': list_params(item['inputs'])
        }

    return function_map
