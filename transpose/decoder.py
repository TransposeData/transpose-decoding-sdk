import json

from transpose.sql.test import test_query
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.exceptions import DecoderConfigError
from transpose.utils.address import to_checksum_address


class Decoder:
    """
    The Decoder class is used to stream events and contract calls for a contract that uses a 
    given ABI.
    """
    
    def __init__(self, 
                 transpose_api_key: str=None,
                 contract_address: str=None,
                 abi: dict=None,
                 abi_path: str=None,
                 chain: str='ethereum') -> None:

        """
        Initialize the decoder class. Doing so requires a valid API key, a valid contract address, and 
        a valid ABI, supplied as either a dict or a path to a JSON file.

        :param transpose_api_key: The API key for Transpose.
        :param contract_address: The contract address.
        :param abi: The ABI, supplied as a dict.
        :param abi_path: The path to the ABI, supplied as a JSON file.
        """

        # validate API key
        if transpose_api_key is None or not isinstance(transpose_api_key, str) or len(transpose_api_key) <= 0: 
            raise DecoderConfigError('Transpose API key is required')
        self.transpose_api_key = transpose_api_key
        
        # run test query
        send_transpose_sql_request(
            api_key=self.transpose_api_key,
            query=test_query()
        )

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
        elif not all([isinstance(x, dict) for x in self.abi]): raise DecoderConfigError('ABI must be a list of dicts')

        # validate chain
        self.chain = chain.lower()
        if self.chain not in ['ethereum', 'polygon', 'goerli']:
            raise DecoderConfigError('Invalid chain')

        # initialize stream
        self.stream = None


    def stream_all_events(self, 
                          block_start: int=0,
                          block_end: int=None,
                          limit: int=None) -> None:

        """
        Initiate a stream of all the events for a given contract.

        :param block_start: The starting block number.
        :param block_end: The ending block number.
        :param limit: The maximum number of events to return.
        """
        
        pass


    def stream_events(self, event_name: str,
                      block_start: int=0,
                      block_end: int=None,
                      limit: int=None) -> None:
        
        pass


    def stream_all_calls(self,
                         block_start: int=0,
                         block_end: int=None,
                         limit: int=None,
                         transactions_only: bool=False) -> None:
            
        pass


    def stream_calls(self, function_name: str,
                     block_start: int=0,
                     block_end: int=None,
                     limit: int=None,
                     transactions_only: bool=False) -> None:
        
        pass