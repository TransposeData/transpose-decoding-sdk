from transpose.contract import TransposeDecodedContract


def descending_events_demo(api_key: str) -> None:
    """
    This demo shows how to stream all events to a contract in descending
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
    stream = contract.stream_events(
        start_block=4753925,
        order='desc'
    )

    # iterate over stream
    for event in stream:
        print('{} ({}, {})'.format(
            event['item']['event_name'],
            event['context']['block_number'],
            event['context']['log_index']
        ))