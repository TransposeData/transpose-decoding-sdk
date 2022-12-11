from typing import Tuple, List
from web3 import Web3

from transpose.stream.base import Stream
from transpose.sql.events import all_logs_query
from transpose.utils.exceptions import StreamConfigError
from transpose.utils.request import send_transpose_sql_request


class EventStream(Stream):
    """
    The EventStream class implements the Stream class to stream events
    from a contract. See the Stream class for more information on the 
    interface for this class.
    """

    def __init__(self, api_key: str, contract_address: str, abi: dict,
                 event_name: str=None,
                 start_block: int=0,
                 end_block: int=None,
                 scroll_iterator: bool=False,
                 scroll_delay: int=3) -> None:

        """
        Initialize the stream.

        :param api_key: The API key
        :param contract_address: The contract address.
        :param abi: The contract ABI.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param scroll_iterator: Whether to use a scroll iterator.
        :param scroll_delay: The delay between scroll requests.
        """

        super().__init__(
            api_key=api_key,
            start_block=start_block,
            end_block=end_block,
            scroll_iterator=scroll_iterator,
            scroll_delay=scroll_delay
        )

        self.contract_address = contract_address
        self.abi = abi

        # convert event name to signature
        self.topic_0 = None
        if event_name is not None:
            signature_prehash = ''
            for item in self.abi:

                # check type
                if 'type' not in item or item['type'] not in ['event', 'constructor', 'fallback', 'function']: 
                    raise StreamConfigError('Invalid ABI (missing type field)')
                elif item['type'] != 'event': continue

                # check anonymous
                elif 'anonymous' not in item or not isinstance(item['anonymous'], bool): 
                    raise StreamConfigError('Invalid ABI (missing anonymous field)')
                elif item['anonymous']: continue

                # check name
                elif 'name' not in item or not isinstance(item['name'], str) or len(item['name']) == 0:
                    raise StreamConfigError('Invalid ABI (missing name field)')
                elif item['name'] != event_name: continue

                # check inputs
                if 'inputs' not in item or not isinstance(item['inputs'], list): 
                    raise StreamConfigError('Invalid ABI (missing inputs field)')

                # build signature prehash
                signature_prehash += item['name'] + '('
                for input in item['inputs']:
                    if 'type' not in input or not isinstance(input['type'], str) or len(input['type']) == 0:
                        raise StreamConfigError('Invalid ABI (missing input type field)')
                    signature_prehash += input['type'] + ','
                signature_prehash = signature_prehash[:-1] + ')'
                break
        
            # hash signature prehash
            if signature_prehash == '':
                raise StreamConfigError('Invalid event name')
            self.topic_0 = Web3.keccak(text=signature_prehash).hex()


    def reset(self, start_block: int) -> dict:
        """
        Reset the stream state to the default state. The default stream
        state is simply the start block and the zero log index.

        :param start_block: The block to reset the stream to.
        """

        return {
            'block': start_block,
            'log_index': 0
        }

    
    def fetch(self, state: dict,
              end_block: int=None,
              limit: int=None) -> Tuple[List[dict], dict]:

        """
        Fetch the next set of logs from the stream and update the 
        state.

        :param state: The current stream state.
        :param end_block: The block to stop fetching at, exclusive.
        :param limit: The maximum number of events to fetch.
        """

        raw_data = send_transpose_sql_request()




    def decode(self, data: dict) -> dict:
        return data