from eth_event import get_topic_map, decode_log
from typing import Tuple, List

from transpose.stream.base import Stream
from transpose.sql.events import events_query
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
                 live_iterate: bool=False,
                 live_iterate_refresh_interval: int=3) -> None:

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

        # build topic map
        try: self.topic_map = get_topic_map(self.abi)
        except Exception as e:
            raise StreamConfigError('Invalid ABI') from e

        # get target event
        self.event_signature = None
        if event_name is not None:
            self.event_signature = [k for k, v in self.topic_map.items() if v['name'] == event_name]
            if len(self.event_signature) == 0: raise StreamConfigError('Invalid event name')
            self.event_signature = self.event_signature[0]
            

    def reset(self, start_block: int) -> dict:
        """
        Reset the stream state to the default state. The default stream
        state is simply the start block and the zero log index.

        :param start_block: The block to reset the stream to.
        :return: The default stream state.
        """

        return {
            'block_number': start_block,
            'log_index': 0
        }

    
    def fetch(self, state: dict,
              stop_block: int=None,
              limit: int=None) -> Tuple[List[dict], dict]:

        """
        Fetch the next set of raw events for the stream and update the 
        stream state.

        :param state: The current stream state.
        :param stop_block: The block to stop fetching at, exclusive.
        :param limit: The maximum number of events to fetch.
        """

        # build query
        query = events_query(
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
            'event': {
                d['name']: d['value'] 
                for d in decoded_log['data']
            }
        }