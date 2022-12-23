from abc import ABC, abstractmethod
from typing import List, Tuple
import time

from transpose.utils.exceptions import StreamError


class Stream(ABC):
    """
    The Stream class is an abstract base class for all stream objects. Each stream
    implementation must inherit from this class and implement the fetch() and
    decode() methods. Then, you can continuously call the next() method to
    retrieve the next batch of data from the stream. You may also use the stream
    as an iterator, which will return a single item on each iteration.
    """

    def __init__(self, api_key: str,
                 start_block: int=0,
                 end_block: int=None,
                 order: str='asc',
                 live_stream: bool=False,
                 live_refresh_interval: int=3) -> None:

        """
        Initialize the stream.

        :param api_key: The API key for the Transpose API.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param order: The order to stream the events in.
        :param live_stream: Whether to scroll the iterator when reaches live.
        :param live_refresh_interval: The delay between scroll attempts in seconds.
        """

        self.api_key = api_key
        self.start_block = start_block
        self.end_block = end_block
        self.order = order
        self.live_stream = live_stream
        self.live_refresh_interval = live_refresh_interval
        self.__state = None
        self.__it_idx = None
        self.__it_data = None

        # validate order
        if order not in ['asc', 'desc']:
            raise StreamError('Invalid order (must be "asc" or "desc")')

        # validate block range
        if not isinstance(start_block, int) or start_block < 0:
            raise StreamError('Invalid start block')
        elif end_block is not None:
            if not isinstance(end_block, int): raise StreamError('Invalid end block')
            elif order == 'asc' and end_block < start_block: raise StreamError('Invalid block range')
            elif order == 'desc' and end_block > start_block: raise StreamError('Invalid block range')

        # validate scroll iterator
        if not isinstance(live_stream, bool):
            raise StreamError('Invalid scroll iterator')
        elif live_stream and end_block is not None:
            raise StreamError('Cannot scroll iterator when end block is specified')

        # validate scroll delay
        if not isinstance(live_refresh_interval, int) or live_refresh_interval < 0:
            raise StreamError('Invalid scroll delay')


    def __iter__(self) -> 'Stream':
        """
        Return the stream object as an iterator.

        :return: The stream object.
        """

        return self


    def next(self, 
             limit: int=100) -> List[dict]:
             
        """
        Return the next batch of data from the stream.

        :param limit: The maximum number of items to return.
        :return: The next batch of data.
        """

        return self.__load_next_batch(limit)

    
    def __next__(self) -> dict:
        """
        Return the next item from the stream.

        :return: The next item.
        """

        try:

            # check if we have any data left
            if self.__it_idx is None or self.__it_idx >= len(self.__it_data):
                self.__it_data = self.__load_next_batch(None)
                self.__it_idx = 0

                # if scroll iterator is enabled, wait for data
                if len(self.__it_data) == 0 and self.live_stream:
                    while len(self.__it_data) == 0:
                        time.sleep(self.live_refresh_interval)
                        self.__it_data = self.__load_next_batch(None)
                
                # otherwise, raise StopIteration
                elif len(self.__it_data) == 0:
                    raise StopIteration
                
            # get next item
            item = self.__it_data[self.__it_idx]
            self.__it_idx += 1
            return item

        except KeyboardInterrupt:
            raise StopIteration


    def __load_next_batch(self, limit: int) -> List[dict]:
        """
        Private implementation to fetch the next batch of data from the stream.

        :param limit: The maximum number of items to return.
        """

        # set initial state
        if self.__state is None:
            self.__state = self.reset(self.start_block)

        # fetch data
        data, self.__state = self.fetch(
            state=self.__state,
            stop_block=self.end_block,
            order=self.order,
            limit=limit
        )

        # decode data
        decoded_data = []
        for item in data:
            decoded_item = self.decode(item)
            if decoded_item is not None:
                decoded_data.append(decoded_item)

        return decoded_data


    @abstractmethod
    def reset(self, start_block: int) -> dict:
        """
        Reset the stream by returning the default stream state as defined by the 
        implementation. This is an abstract method that must be implemented by
        the child class.

        :param start_block: The block to start streaming from, exclusive.
        :return: The default stream state.
        """

        raise NotImplementedError


    @abstractmethod
    def fetch(self, state: dict,
              stop_block: int=None,
              order: str='asc',
              limit: int=None) -> Tuple[List[dict], dict]:
              
        """
        Retrieve the next batch of raw data from the stream. This is an abstract
        method that must be implemented by the child class.

        :param state: The current stream state.
        :param stop_block: The block to stop streaming at, exclusive.
        :param order: The order to stream the events in.
        :param limit: The maximum number of items to return in the batch.
        :return: A tuple containing the batch data and the resulting state.
        """

        raise NotImplementedError

    
    @abstractmethod
    def decode(self, data: dict) -> dict:
        """
        Decode a single item from the stream. This is an abstract method that
        must be implemented by the child class.

        :param data: The data to decode.
        """

        raise NotImplementedError