from abc import ABC, abstractmethod
from typing import List, Tuple
import time

from transpose.utils.exceptions import StreamConfigError


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
                 scroll_iterator: bool=False,
                 scroll_delay: int=3) -> None:

        """
        Initialize the stream.

        :param api_key: The API key for the Transpose API.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param scroll_iterator: Whether to scroll the iterator when reaches live.
        :param scroll_delay: The delay between scroll attempts in seconds.
        """

        self.api_key = api_key
        self.start_block = start_block
        self.end_block = end_block
        self.scroll_iterator = scroll_iterator
        self.scroll_delay = scroll_delay
        self.__state = None
        self.__it_idx = None
        self.__it_data = None

        # validate block range
        if not isinstance(start_block, int) or start_block < 0:
            raise StreamConfigError('Invalid start block')
        elif end_block is not None and (not isinstance(end_block, int) or end_block < start_block):
            raise StreamConfigError('Invalid end block')

        # validate scroll iterator
        if not isinstance(scroll_iterator, bool):
            raise StreamConfigError('Invalid scroll iterator')
        elif scroll_iterator and end_block is not None:
            raise StreamConfigError('Cannot scroll iterator when end block is specified')

        # validate scroll delay
        if not isinstance(scroll_delay, int) or scroll_delay < 0:
            raise StreamConfigError('Invalid scroll delay')


    def __iter__(self) -> 'Stream':
        """
        Return the stream object as an iterator.

        :return: The stream object.
        """

        return self


    def next(self, limit: int=100) -> List[dict]:
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

        # check if we have any data left
        if self.__it_idx is None or self.__it_idx >= len(self.__it_data):
            self.__it_data = self.__load_next_batch(None)
            self.__it_idx = 0

            # if scroll iterator is enabled, wait for data
            if len(self.__it_data) == 0 and self.scroll_iterator:
                while len(self.__it_data) == 0:
                    time.sleep(self.scroll_delay)
                    self.__it_data = self.__load_next_batch(None)
            
            # otherwise, raise StopIteration
            elif len(self.__it_data) == 0:
                raise StopIteration
            
        # get next item
        item = self.__it_data[self.__it_idx]
        self.__it_idx += 1
        return item


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
            end_block=self.end_block,
            limit=limit
        )

        # decode data
        return [
            self.decode(item) 
            for item in data
        ]


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
              end_block: int=None,
              limit: int=None) -> Tuple[List[dict], dict]:
              
        """
        Retrieve the next batch of raw data from the stream. This is an abstract
        method that must be implemented by the child class.

        :param state: The current stream state.
        :param end_block: The block to stop streaming at, exclusive.
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