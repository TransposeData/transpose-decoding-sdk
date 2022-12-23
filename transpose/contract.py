import json

from transpose.stream.base import Stream
from transpose.stream.event import EventStream
from transpose.stream.call import CallStream
from transpose.sql.general import latest_block_query
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.exceptions import ContractError
from transpose.utils.address import to_checksum_address


class TransposeDecodedContract:
    """
    The TransposeDecodedContract class is used to stream decoded events and contract calls for a contract
    given its contract address and ABI. The class is initialized with a valid API key, contract address, and ABI.
    The class can then be used to stream decoded events and contract calls by either calling the stream_events()
    or stream_calls() methods with a number of parameters. The stream_events() method will return an EventStream
    object, which can be used to stream decoded events. The stream_calls() method will return a CallStream object,
    which can be used to stream decoded contract calls.

    The stream can then be used to get the next decoded event or contract call with the next() method. The stream
    can also be used as an iterator, which will return the next decoded event or contract call on each iteration.
    """
    
    def __init__(self, contract_address: str,
                 abi: dict=None, 
                 abi_path: str=None,
                 chain: str='ethereum',
                 api_key: str=None) -> None:

        """
        Initialize the TransposeDecodedContract class with a valid target contract and
        Transpose API key.

        :param contract_address: The contract address.
        :param abi: The ABI, supplied as a dict.
        :param abi_path: The path to the ABI, supplied as a JSON file.
        :param chain: The chain the contract is deployed on.
        :param api_key: The API key for the Transpose API.
        """

        # validate contract address
        self.contract_address = to_checksum_address(contract_address)
        if self.contract_address is None: raise ContractError('Invalid contract address')

        # validate ABI
        if abi is None and abi_path is None: raise ContractError('ABI is required')
        elif abi is not None and abi_path is not None: raise ContractError('Only one of ABI or ABI path can be supplied')
        elif abi is not None: self.abi = abi
        elif abi_path is not None:
            try: self.abi = json.load(open(abi_path))
            except: raise ContractError('Invalid ABI path')

        # validate ABI object
        if not isinstance(self.abi, list): raise ContractError('ABI must be a list of dicts')
        elif not all([isinstance(item, dict) for item in self.abi]): raise ContractError('ABI must be a list of dicts')

        # validate chain
        self.chain = chain
        if chain not in ['ethereum', 'goerli', 'polygon']: 
            raise ContractError('Invalid chain')

        # validate API key
        if api_key is None or not isinstance(api_key, str) or len(api_key) <= 0: 
            raise ContractError('Transpose API key is required')
        self.api_key = api_key
        
        # run test query
        send_transpose_sql_request(
            api_key=self.api_key,
            query=latest_block_query('ethereum')
        )


    def stream_events(self, 
                      event_name: str=None,
                      start_block: int=None,
                      end_block: int=None,
                      order: str='asc',
                      live_stream: bool=False,
                      live_refresh_interval: int=3) -> Stream:
        
        """
        Initiate a stream for contract events.

        :param event_name: The name of the event.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param order: The order to stream the events in.
        :param live_stream: Whether to stream live data.
        :param live_refresh_interval: The interval for refreshing the data in seconds when live.
        :return: A Stream object.
        """

        # check order
        if order not in ['asc', 'desc']: 
            raise ContractError('Invalid order (must be one of "asc" or "desc")')
        elif order == 'desc' and live_stream:
            raise ContractError('Cannot stream in descending order when live')

        # set start and stop blocks
        next_block = self.__get_latest_block() + 1
        if live_stream: 
            start_block = min(start_block, next_block) if start_block is not None else next_block
            end_block = None
        else:
            if order == 'asc':
                start_block = max(start_block, 0) if start_block is not None else 0
                end_block = min(end_block, next_block) if end_block is not None else next_block
                if start_block > end_block: raise ContractError('Invalid start and end blocks')
            else:
                start_block = min(start_block, next_block) if start_block is not None else next_block
                end_block = max(end_block, 0) if end_block is not None else 0
                if start_block < end_block: raise ContractError('Invalid start and end blocks')

        # return stream
        return EventStream(
            api_key=self.api_key,
            chain=self.chain,
            contract_address=self.contract_address,
            abi=self.abi,
            event_name=event_name,
            start_block=start_block,
            end_block=end_block,
            order=order,
            live_stream=live_stream,
            live_refresh_interval=live_refresh_interval
        )


    def stream_calls(self, 
                     function_name: str=None,
                     start_block: int=None,
                     end_block: int=None,
                     order: str='asc',
                     live_stream: bool=False,
                     live_refresh_interval: int=3) -> Stream:
        
        """
        Initiate a stream for contract calls.

        :param function_name: The name of the function.
        :param start_block: The block to start streaming from, inclusive.
        :param end_block: The block to stop streaming at, exclusive.
        :param order: The order to stream the calls in.
        :param live_stream: Whether to stream live data.
        :param live_refresh_interval: The interval for refreshing the data in seconds when live.
        :return: A Stream object.
        """

        # check order
        if order not in ['asc', 'desc']: 
            raise ContractError('Invalid order (must be one of "asc" or "desc")')
        elif order == 'desc' and live_stream:
            raise ContractError('Cannot stream in descending order when live')

        # set start and stop blocks
        next_block = self.__get_latest_block() + 1
        if live_stream: 
            start_block = min(start_block, next_block) if start_block is not None else next_block
            end_block = None
        else:
            if order == 'asc':
                start_block = max(start_block, 0) if start_block is not None else 0
                end_block = min(end_block, next_block) if end_block is not None else next_block
                if start_block > end_block: raise ContractError('Invalid start and end blocks')
            else:
                start_block = min(start_block, next_block) if start_block is not None else next_block
                end_block = max(end_block, 0) if end_block is not None else 0
                if start_block < end_block: raise ContractError('Invalid start and end blocks')

        # return stream
        return CallStream(
            api_key=self.api_key,
            chain=self.chain,
            contract_address=self.contract_address,
            abi=self.abi,
            function_name=function_name,
            start_block=start_block,
            end_block=end_block,
            order=order,
            live_stream=live_stream,
            live_refresh_interval=live_refresh_interval
        )
    

    def __get_latest_block(self) -> int:
        """
        Get the latest block number for the current chain.

        :return: The latest block number.
        """

        return send_transpose_sql_request(
            api_key=self.api_key,
            query=latest_block_query(self.chain)
        )[0]['block_number']