from transpose.contract import TransposeDecodedContract
from web3 import Web3, HTTPProvider
import json
import time


def web3py_weth_events_benchmark(rpc_api_url: str, transpose_api_key: str, from_block: int, to_block: int) -> None:
    """
    Benchmark Web3.py library for streaming decoded Ethereum events with a RPC
    API against the Transpose Decoding SDK with a Transpose API key.

    :param rpc_api_url: The RPC API URL to connect to.
    :param transpose_api_key: The Transpose API key to use.
    :param from_block: The block to start streaming events from.
    :param to_block: The block to stop streaming events at.
    """

    # run benchmark on Web3.py
    print('\rBenchmarking Web3.py... ', end='')
    start_time_web3py = time.time()
    web3py_events_streamed = run_web3py_benchmark(rpc_api_url, from_block, to_block)
    end_time_web3py = time.time()
    print('Done.')

    # run benchmark on Transpose
    print('\rBenchmarking Transpose... ', end='')
    start_time_transpose = time.time()
    transpose_events_streamed = run_transpose_benchmark(transpose_api_key, from_block, to_block)
    end_time_transpose = time.time()
    print('Done.')

    # print results
    print('Events streamed: {}'.format(web3py_events_streamed))
    print('\n========== Web3.py ==========')
    print('Time elapsed: {} seconds'.format(end_time_web3py - start_time_web3py))
    print('Events per second: {}'.format(web3py_events_streamed / (end_time_web3py - start_time_web3py)))
    print('\n========== Transpose ==========')
    print('Time elapsed: {} seconds'.format(end_time_transpose - start_time_transpose))
    print('Events per second: {}'.format(transpose_events_streamed / (end_time_transpose - start_time_transpose)))


def run_web3py_benchmark(rpc_api_url: str, from_block: int, to_block: int) -> int:
    """
    Run the Web3.py component of the benchmark.

    :param rpc_api_url: The RPC API URL.
    :param from_block: The block to start streaming events from.
    :param to_block: The block to stop streaming events at.
    :return: The number of events streamed.
    """

    # connect to Ethereum node
    web3 = Web3(HTTPProvider(rpc_api_url))

    # load ABI
    with open('abi/weth-abi.json') as f:
        weth_abi = json.load(f)

    # create contract object
    contract = web3.eth.contract(
        address='0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
        abi=weth_abi
    )

    # stream events in batches of 2000 blocks
    total_events_streamed = 0
    for block in range(from_block, to_block, 2000):
        filter = contract.events.Transfer.createFilter(
            fromBlock=block,
            toBlock=block + 2000
        )

        # stream events
        total_events_streamed += len(filter.get_all_entries())

    return total_events_streamed


def run_transpose_benchmark(api_key: str, from_block: int, to_block: int) -> int:
    """
    Run the Transpose component of the benchmark.

    :param api_key: The API key to use for the Transpose API.
    :param from_block: The block to start streaming events from.
    :param to_block: The block to stop streaming events at.
    :return: The number of events streamed.
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
        start_block=from_block,
        end_block=to_block,
        event_name='Transfer'
    )
    
    # iterate over stream
    total_events_streamed = 0
    for _ in stream: total_events_streamed += 1
    return total_events_streamed
