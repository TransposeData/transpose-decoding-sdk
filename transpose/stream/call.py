from eth_event import get_topic_map, decode_log
from typing import Tuple, List
from web3 import Web3

from transpose.stream.base import Stream
from transpose.sql.events import logs_query
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
                 scroll_iterator: bool=False,
                 scroll_delay: int=3,
                 include_internal_calls: bool=True) -> None:

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
        :param include_internal_calls: Whether to include internal calls.
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
        self.include_internal_calls = include_internal_calls

        # convert function name to selector
        self.function_selector = None
        if function_name is not None:
            pass