from transpose.contract import TransposeDecodedContract


def historical_weth_calls_demo(api_key: str) -> None:
    """
    This demo shows how to stream historical calls from the Wrapped
    Ether contract. To do so, it initializes a stream of all withdrawal
    calls from the Wrapped Ether contract, starting at block 15M. It 
    then prints the next 10 calls to the console.

    :param api_key: Your Transpose API key.
    """
    
    # initialize OpenSea Seaport contract
    contract = TransposeDecodedContract(
        contract_address='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2',
        abi_path='abi/weth-abi.json',
        chain='ethereum',
        api_key=api_key
    )

    # build call stream
    stream = contract.stream_calls(
        function_name='withdraw',
        start_block=15000000
    )

    # get first 10 calls
    print(stream.next(10))
    