from transpose.contract import TransposeDecodedContract


def live_seaport_calls_demo(api_key: str) -> None:
    """
    This demo shows how to stream live calls from the OpenSea Seaport
    contract. To do so, it initializes a stream of all calls from the
    OpenSea Seaport contract, starting at the latest block. It then
    iterates over the stream and prints each call to the console as they
    are received the Transpose backend.

    :param api_key: Your Transpose API key.
    """
    
    # initialize OpenSea Seaport contract
    contract = TransposeDecodedContract(
        contract_address='0x00000000006c3852cbEf3e08E8dF289169EdE581',
        abi_path='abi/opensea-seaport-abi.json',
        chain='ethereum',
        api_key=api_key
    )

    # build call stream
    stream = contract.stream_calls()

    # iterate over stream
    for call in stream:
        print(call)