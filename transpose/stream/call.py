from typing import Tuple, List

from transpose.stream.base import Stream
from transpose.sql.calls import calls_query
from transpose.utils.exceptions import StreamConfigError
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.decode import build_function_map


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
                 live_iterator: bool=False,
                 live_iterator_refresh_interval: int=3) -> None:

        """
        Initialize the stream.

        :param api_key: The API key.
        :param chain: The chain name.
        :param contract_address: The contract address.
        :param abi: The contract ABI.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param live_iterator: Whether to continuously iterate over live data.
        :param live_iterator_refresh_interval: The interval between refreshing the data when live in seconds.
        """

        super().__init__(
            api_key=api_key,
            start_block=start_block,
            end_block=end_block,
            live_iterator=live_iterator,
            live_iterator_refresh_interval=live_iterator_refresh_interval
        )

        self.chain = chain
        self.contract_address = contract_address
        self.abi = abi

        # build function map
        try: self.function_map = build_function_map(self.abi)
        except Exception as e:
            raise StreamConfigError('Invalid ABI') from e

        # get target function selector
        self.function_selector = None
        if function_name is not None:
            matching_function_selectors = [k for k, v in self.function_map.items() if v['name'] == function_name]
            if len(matching_function_selectors) != 1: raise StreamConfigError('Invalid function name')
            self.function_selector = matching_function_selectors[0]

    
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
            state['trace_index'] = data[-1]['trace_index'] + 1

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
                'contract_address': 1
            }
        }