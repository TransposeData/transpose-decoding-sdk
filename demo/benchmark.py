from transpose.contract import TransposeDecodedContract
import time


def benchmark_demo(api_key: str) -> None:
    """
    This benchmark demo tests the speed of the Transpose Decoding SDK
    by measuring the number of events per second that can be streamed
    from the Ethereum WETH contract. To do so, it initializes a stream
    of all events from the WETH contract, starting at block 0 and ending
    at the latest block (live_stream=False). It then iterates over the
    stream and prints the number of events per second to the console.

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
        start_block=0,
        live_stream=False
    )

    # iterate over stream
    t1 = time.time()
    counter = 0
    for _ in stream:
        counter += 1
        print('\rEPS: {}\t'.format(round(counter / (time.time() - t1), 3)), end='')