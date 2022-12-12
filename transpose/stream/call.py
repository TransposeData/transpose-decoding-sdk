from typing import Tuple, List
from web3 import Web3

from transpose.stream.base import Stream
from transpose.sql.calls import calls_query
from transpose.utils.exceptions import StreamConfigError
from transpose.utils.request import send_transpose_sql_request


class CallStream(Stream):
    """
    The CallStream class implements the Stream class to stream calls
    from a contract. See the Stream class for more information on the 
    interface for this class.
    """

    def __init__(self, api_key: str, chain: str, contract_address: str, abi: dict,
                 function_name: str=None,
                 start_block: int=0,
                 end_block: int=None,
                 live_iterate: bool=False,
                 live_iterate_refresh_interval: int=3,
                 include_internal_calls: bool=True) -> None:

        """
        Initialize the stream.

        :param api_key: The API key.
        :param chain: The chain name.
        :param contract_address: The contract address.
        :param abi: The contract ABI.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param live_iterate: Whether to continuously iterate over live data.
        :param live_iterate_refresh_interval: The interval between refreshing the data when live in seconds.
        :param include_internal_calls: Whether to include internal calls.
        """

        super().__init__(
            api_key=api_key,
            start_block=start_block,
            end_block=end_block,
            live_iterate=live_iterate,
            live_iterate_refresh_interval=live_iterate_refresh_interval
        )

        self.chain = chain
        self.contract_address = contract_address
        self.abi = abi
        self.include_internal_calls = include_internal_calls

        # convert function name to selector
        self.function_selector = None
        if function_name is not None:
            signature_prehash = ''
            for item in self.abi:
                    
                # check type
                if 'type' not in item or item['type'] not in ['event', 'constructor', 'fallback', 'function']: 
                    raise StreamConfigError('Invalid ABI (missing type field)')
                elif item['type'] != 'function': continue

                # check name
                elif 'name' not in item or not isinstance(item['name'], str) or len(item['name']) == 0:
                    raise StreamConfigError('Invalid ABI (missing name field)')
                elif item['name'] != function_name: continue

                # check inputs
                if 'inputs' not in item or not isinstance(item['inputs'], list): 
                    raise StreamConfigError('Invalid ABI (missing inputs field)')
                    
                # build signature prehash
                function_types = []
                for input in item['inputs']:
                    if 'type' not in input or not isinstance(input['type'], str) or len(input['type']) == 0:
                        raise StreamConfigError('Invalid ABI (missing input type field)')
                    function_types.append(input['type'])
                signature_prehash = item['name'] + '(' + ','.join(function_types) + ')'
                break

            # hash signature prehash
            if signature_prehash == '':
                raise StreamConfigError('Invalid function name')
            self.function_selector = Web3.sha3(text=signature_prehash).hex()[:10]
        
        # build contract object
        self.contract = Web3().eth.contract(
            address=self.contract_address,
            abi=self.abi
        )

    
    def reset(self, start_block: int) -> dict:
        """
        Reset the stream state to the default state. The default stream
        state is simply the start block, the zero transaction position,
        and the zero trace index.

        :param start_block: The block to reset the stream to.
        :return: The default stream state.
        """

        return {
            'block_number': start_block,
            'transaction_position': 0,
            'trace_index': 0
        }


    def fetch(self, state: dict,
              stop_block: int=None,
              limit: int=None) -> Tuple[List[dict], dict]:

        """
        Fetch the next set of raw calls for the stream and update
        the stream state.

        :param state: The current stream state.
        :param stop_block: The block to stop fetching at, exclusive.
        :param limit: The maximum number of calls to fetch.
        """

        # build query
        query = calls_query(
            chain=self.chain,
            contract_address=self.contract_address,
            from_block=state['block_number'],
            from_transaction_position=state['transaction_position'],
            from_trace_index=state['trace_index'],
            function_selector=self.function_selector,
            stop_block=stop_block,
            limit=limit
        )

        # send request
        data = send_transpose_sql_request(
            api_key=self.api_key,
            query=query
        )

        # update state
        if len(data) > 0:
            state['block_number'] = data[-1]['block_number']
            state['transaction_position'] = data[-1]['transaction_position']
            state['trace_index'] = data[-1]['trace_index']

        return data, state


    def decode(self, data: dict) -> dict:
        """
        Decode the raw transaction/trace data into a decoded call. The decoded 
        call is a dictionary with three fields: the item, the context, the input_data,
        and the output_data. The item field contains information on the target
        activity, the context field contains information on the
        context of the activity, and the input_data and output_data fields
        contain the decoded input and output data for the call.

        :param data: The raw transaction/trace data.
        :return: The decoded call data.
        """

        # format decoded log
        return {
            'item': {
                'contract_address': 1}
        }