from eth_event import get_topic_map, decode_log
from typing import Tuple, List
from web3 import Web3

from transpose.stream.base import Stream
from transpose.sql.events import logs_query
from transpose.utils.exceptions import StreamConfigError
from transpose.utils.request import send_transpose_sql_request


class EventStream(Stream):
    """
    The EventStream class implements the Stream class to stream events
    from a contract. See the Stream class for more information on the 
    interface for this class.
    """

    def __init__(self, api_key: str, chain: str, contract_address: str, abi: dict,
                 event_name: str=None,
                 start_block: int=0,
                 end_block: int=None,
                 scroll_iterator: bool=False,
                 scroll_delay: int=3) -> None:

        """
        Initialize the stream.

        :param api_key: The API key.
        :param chain: The chain name.
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

        self.chain = chain
        self.contract_address = contract_address
        self.abi = abi

        # convert event name to event signature
        self.event_signature = None
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
            self.event_signature = Web3.keccak(text=signature_prehash).hex()

        # build topic map
        self.topic_map = get_topic_map(
            abi=self.abi
        )


    def reset(self, start_block: int) -> dict:
        """
        Reset the stream state to the default state. The default stream
        state is simply the start block and the zero log index.

        :param start_block: The block to reset the stream to.
        """

        return {
            'block_number': start_block,
            'log_index': 0
        }

    
    def fetch(self, state: dict,
              stop_block: int=None,
              limit: int=None) -> Tuple[List[dict], dict]:

        """
        Fetch the next set of logs from the stream and update the 
        state.

        :param state: The current stream state.
        :param stop_block: The block to stop fetching at, exclusive.
        :param limit: The maximum number of events to fetch.
        """

        # build query
        query = logs_query(
            chain=self.chain,
            contract_address=self.contract_address,
            from_block=state['block_number'],
            from_log_index=state['log_index'],
            topic_0=self.event_signature,
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
            state['log_index'] = data[-1]['log_index'] + 1

        return data, state


    def decode(self, data: dict) -> dict:
        """
        Decode the raw log data into a decoded event. The decoded event
        is a dictionary with three fields: the item, the context, and
        the data. The item field contains information on the target
        activity, the context field contains information on the
        context of the activity, and the data field contains the decoded
        data from the log.

        :param data: The raw log data.
        :return: The decoded log.
        """

        # format raw log
        log = {
            'address': data['address'],
            'topics': [],
            'data': data['data']
        }

        # add topics
        for i in range(0, 4):
            if data[f'topic_{i}'] is not None:
                log['topics'].append(data[f'topic_{i}'])

        # decode log
        decoded_log = decode_log(log, self.topic_map)

        # format decoded log
        return {
            'item': {
                'contract_address': decoded_log['address'],
                'event_name': decoded_log['name']
            },
            'context': {
                'timestamp': data['timestamp'],
                'block_number': data['block_number'],
                'log_index': data['log_index'],
                'transaction_hash': data['transaction_hash'],
                'transaction_position': data['transaction_position'],
                'confirmed': data['__confirmed']
            },
            'data': {
                d['name']: d['value'] 
                for d in decoded_log['data']
            }
        }