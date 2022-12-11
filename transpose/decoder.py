import json

from transpose.sql.test import TEST_QUERY
from transpose.utils.request import send_transpose_sql_request
from transpose.utils.exceptions import DecoderConfigError


class Decoder:
    
    def __init__(self, 
                 transpose_api_key: str=None,
                 contract_address: str=None,
                 abi: dict=None,
                 abi_path: str=None) -> None:

        """
        Initialize the decoder class. Doing so requires a valid API key, a valid contract address, and 
        a valid ABI, supplied as a dict or a path to a JSON file.

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
            query=TEST_QUERY
        )

        # validate contract address
        if contract_address is None or not isinstance(contract_address, str) or len(contract_address) <= 0:
            