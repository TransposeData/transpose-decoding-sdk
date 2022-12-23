from typing import Tuple, List

from transpose.stream.base import Stream
from transpose.sql.events import events_query
from transpose.utils.exceptions import StreamError
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.decode import build_topic_map, decode_hex_data, resolve_decoded_data
from transpose.utils.time import to_iso_timestamp


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
                 order: str='asc',
                 live_stream: bool=False,
                 live_refresh_interval: int=3) -> None:

        """
        Initialize the stream.

        :param api_key: The API key.
        :param chain: The chain name.
        :param contract_address: The contract address.
        :param abi: The contract ABI.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param order: The order to stream the events in.
        :param live_stream: Whether to stream live data.
        :param live_refresh_interval: The interval for refreshing the data in seconds when live.
        """

        super().__init__(
            api_key=api_key,
            start_block=start_block,
            end_block=end_block,
            order=order,
            live_stream=live_stream,
            live_refresh_interval=live_refresh_interval
        )

        self.chain = chain
        self.contract_address = contract_address
        self.abi = abi

        # build topic map
        try: self.topic_map = build_topic_map(self.abi)
        except Exception as e: raise StreamError('Invalid ABI') from e

        # get target event signature
        self.event_signature = None
        if event_name is not None:
            matching_event_signatures = [k for k, v in self.topic_map.items() if v['name'] == event_name]
            if len(matching_event_signatures) != 1: raise StreamError('Invalid event name')
            self.event_signature = matching_event_signatures[0]
            

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
              order: str='asc',
              limit: int=None) -> Tuple[List[dict], dict]:

        """
        Fetch the next set of raw events for the stream and update the 
        stream state.

        :param state: The current stream state.
        :param stop_block: The block to stop fetching at, exclusive.
        :param order: The order to fetch the events in.
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
            order=order,
            limit=limit
        )

        # send request
        data = send_transpose_sql_request(
            api_key=self.api_key,
            query=query
        )

        # update state
        if len(data) > 0:
            if order == 'asc':
                state['block_number'] = data[-1]['block_number']
                state['log_index'] = data[-1]['log_index'] + 1
            else:
                if data[0]['log_index'] == 0:
                    state['block_number'] = data[-1]['block_number'] - 1
                    state['log_index'] = int(1e9)
                else:
                    state['block_number'] = data[-1]['block_number']
                    state['log_index'] = data[-1]['log_index'] - 1

        return data, state


    def decode(self, data: dict) -> dict:
        """
        Decode the raw log data into a decoded event. The decoded event
        is a dictionary with three fields: the item, the context, and
        the event_data. The item field contains information on the target
        activity, the context field contains information on the context 
        of the activity, and the event_data field contains the decoded
        data from the log.

        :param data: The raw log data.
        :return: The decoded log.
        """

        # check if log is in topic map
        if data['topic_0'] not in self.topic_map: return None
        target_topic = self.topic_map[data['topic_0']]
        
        # decode topics
        try:
            topics_data = '0x' + ''.join(data[f'topic_{i}'][2:] for i in range(1, 4) if data[f'topic_{i}'] is not None)
            decoded_topics = decode_hex_data(target_topic['topics']['types'], topics_data)
            topics_data = resolve_decoded_data(target_topic['topics']['params'], decoded_topics)
        except Exception as e: 
            raise StreamError('Failed to decode log') from e

        # decode data
        try:
            decoded_data = decode_hex_data(target_topic['data']['types'], data['data'])
            data_data = resolve_decoded_data(target_topic['data']['params'], decoded_data)
        except Exception as e: 
            raise StreamError('Failed to decode data') from e

        # order event data
        event_data = dict(sorted(
            {**topics_data, **data_data}.items(), 
            key=lambda item: target_topic['order'].index(item[0])
        ))

        # format decoded log
        return {
            'item': {
                'contract_address': self.contract_address,
                'event_name': target_topic['name']
            },
            'context': {
                'timestamp': to_iso_timestamp(data['timestamp']),
                'block_number': data['block_number'],
                'log_index': data['log_index'],
                'transaction_hash': data['transaction_hash'],
                'transaction_position': data['transaction_position'],
                'confirmed': data['__confirmed']
            },
            'event_data': event_data
        }