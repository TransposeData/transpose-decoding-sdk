import json

from transpose.stream.base import Stream
from transpose.stream.event import EventStream
from transpose.stream.call import CallStream
from transpose.sql.general import latest_block_query
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.exceptions import DecoderConfigError
from transpose.utils.address import to_checksum_address


class TransposeContractDecoder:
    """
    The TransposeContractDecoder class is used to stream decoded events and contract calls for a contract
    given its contract address and ABI. The class is initialized with a valid API key, contract address, and ABI.
    The class can then be used to stream decoded events and contract calls by either calling the stream_events()
    or stream_calls() methods with a number of parameters. The stream_events() method will return an EventStream
    object, which can be used to stream decoded events. The stream_calls() method will return a CallStream object,
    which can be used to stream decoded contract calls.

    The stream can then be used to get the next decoded event or contract call with the next() method. The stream
    can also be used as an iterator, which will return the next decoded event or contract call on each iteration.
    """
    
    def __init__(self, 
                 api_key: str=None) -> None:

        """
        Initialize the Transpose contract decoder class with a valid Transpose API key. 

        :param api_key: The API key for the Transpose API.
        """

        # validate API key
        if api_key is None or not isinstance(api_key, str) or len(api_key) <= 0: 
            raise DecoderConfigError('Transpose API key is required')
        self.api_key = api_key
        
        # run test query
        send_transpose_sql_request(
            api_key=self.api_key,
            query=latest_block_query('ethereum')
        )


    def load_contract(self, contract_address: str, 
                      abi: dict=None, 
                      abi_path: str=None,
                      chain: str='ethereum') -> None:

        """
        Load a new contract address and ABI.

        :param contract_address: The contract address.
        :param abi: The ABI, supplied as a dict.
        :param abi_path: The path to the ABI, supplied as a JSON file.
        :param chain: The chain the contract is deployed on.
        """

        # validate contract address
        self.contract_address = to_checksum_address(contract_address)
        if self.contract_address is None: raise DecoderConfigError('Invalid contract address')

        # validate ABI
        if abi is None and abi_path is None: raise DecoderConfigError('ABI is required')
        elif abi is not None and abi_path is not None: raise DecoderConfigError('Only one of ABI or ABI path can be supplied')
        elif abi is not None: self.abi = abi
        elif abi_path is not None:
            try: self.abi = json.load(open(abi_path))
            except: raise DecoderConfigError('Invalid ABI path')

        # validate ABI object
        if not isinstance(self.abi, list): raise DecoderConfigError('ABI must be a list of dicts')
        elif not all([isinstance(item, dict) for item in self.abi]): raise DecoderConfigError('ABI must be a list of dicts')

        # validate chain
        self.chain = chain
        if chain not in ['ethereum', 'goerli', 'polygon']: 
            raise DecoderConfigError('Invalid chain')


    def stream_events(self, 
                      event_name: str=None,
                      start_block: int=None,
                      end_block: int=None,
                      scroll_iterator: bool=False,
                      scroll_delay: int=3) -> Stream:
        
        """
        Initiate a stream for contract events.

        :param event_name: The name of the event.
        :param start_block: The starting block number.
        :param end_block: The ending block number.
        :param scroll_iterator: Whether to use a scroll iterator.
        :param scroll_delay: The delay between scroll requests.
        :return: A Stream object.
        """

        # get latest block number if no start block
        if start_block is None:
            start_block = send_transpose_sql_request(
                api_key=self.api_key,
                query=latest_block_query(self.chain)
            )[0]['block_number'] + 1

        # return stream
        return EventStream(
            api_key=self.api_key,
            chain=self.chain,
            contract_address=self.contract_address,
            abi=self.abi,
            event_name=event_name,
            start_block=start_block,
            end_block=end_block,
            scroll_iterator=scroll_iterator,
            scroll_delay=scroll_delay
        )


    def stream_calls(self, 
                     function_name: str=None,
                     start_block: int=None,
                     end_block: int=None,
                     scroll_iterator: bool=False,
                     scroll_delay: int=3,
                     include_internal_calls: bool=True) -> Stream:
        
        pass