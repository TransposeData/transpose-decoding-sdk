from abc import ABC, abstractmethod
from typing import List, Tuple

from transpose.utils.exceptions import StreamConfigError


class Stream(ABC):
    """
    The Stream class is an abstract base class for all stream objects. Each stream
    implementation must inherit from this class and implement the fetch() and
    decode() methods. Then, you can continuously call the next() method to
    retrieve the next batch of data from the stream.
    """

    def __init__(self,
                 start_block: int=0,
                 end_block: int=None) -> None:

        """
        Initialize the stream.

        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, inclusive.
        """

        self.start_block = start_block
        self.end_block = end_block
        self.state = None

        # validate block range
        if not isinstance(start_block, int) or start_block < 0:
            raise StreamConfigError('Invalid start block')
        elif end_block is not None and (not isinstance(end_block, int) or end_block < start_block):
            raise StreamConfigError('Invalid end block')


    def next(self, 
             limit: int=1000) -> List[dict]:

        """
        Get the next batch of data from the stream.

        :param limit: The maximum number of items to return.
        """

        # fetch data
        data, self.cur_block = self.fetch(
            start_block=self.cur_block,
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

        :param start_block: The block to start streaming from, inclusive.

        """

        raise NotImplementedError


    @abstractmethod
    def fetch(self, start_block: int,
              end_block: int=None,
              limit: int=1000) -> Tuple[List[dict], int]:
              
        """
        Retrieve the next batch of raw data from the stream. This is an abstract
        method that must be implemented by the child class.

        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, inclusive.
        :param limit: The maximum number of items to return.
        :return: A tuple containing the data and the next block to stream from.
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