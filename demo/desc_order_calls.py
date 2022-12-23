from transpose.contract import TransposeDecodedContract


def descending_calls_demo(api_key: str) -> None:
    """
    This demo shows how to stream all calls to a contract in descending
    order by block number.

    :param api_key: Your Transpose API key.
    """

    # initialize WETH contract
    contract = TransposeDecodedContract(
        contract_address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        abi_path='abi/weth-abi.json',
        chain='ethereum',
        api_key=api_key
    )

    # build call stream
    stream = contract.stream_calls(
        start_block=4753925,
        order='desc'
    )

    # iterate over stream
    for call in stream:
        print('{} ({}, {}, {})'.format(
            call['item']['function_name'],
            call['context']['block_number'],
            call['context']['transaction_position'],
            call['context']['trace_index']
        ))