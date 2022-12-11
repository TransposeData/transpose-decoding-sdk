from abc import ABC, abstractmethod
from typing import List


class Stream(ABC):
    """
    The Stream class is an abstract base class for all stream objects.
    """

    def __init__(self, abi: dict) -> None:
        """
        Initialize the stream.

        :param abi: The ABI.
        """
        
        self.abi = abi


    def next(self, limit: int=1000) -> List[dict]:
        """
        Get the next batch of data from the stream.

        :param limit: The maximum number of items to return.
        """

        data = self.fetch(limit=limit)
        return [self.decode(item) for item in data]


    @abstractmethod
    def fetch(self, limit: int=1000) -> List[dict]:
        """
        Retrieve the next batch of raw data from the stream.

        :param limit: The maximum number of items to return.
        """

        raise NotImplementedError

    
    @abstractmethod
    def decode(self, data: dict) -> dict:
        """
        Decode a single item from the stream.

        :param data: The data to decode.
        """

        raise NotImplementedError