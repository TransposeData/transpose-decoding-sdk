# Transpose Decoding SDK

The Transpose Decoding SDK is a Python package that makes decoding contract activity on EVM blockchains as simple as possible. Simply specify a contract address and ABI to start streaming historical or live activity across decoded logs, transactions, and traces.

## Features

- **Simple interface**: Simple, minimal code interface to stream decoded events or calls.
- **High performance**: Streaming benchmarked at 3,000+ items per second.
- **Automatic decoding**: Automatically decode inputs/outputs for transactions and traces, and logs for events.
- **Live & historical**: Stream activity in a historical block range or live with a ~3s delay from nodes.
- **Full traces support**: Stream decoded traces (a.k.a. internal transactions) with no added complexity.
- **Multi-chain**: Supports Ethereum, Polygon, and Goerli with additional chains coming soon.
- **Event & function filtering**: Stream all activity from a contract or specify event and function names.

## Setup

### Retrieving an API key

To use the SDK, you will need an API key for Transpose. You can sign up for a free API key by visting the [Transpose App](https://app.transpose.io). If you have any questions on getting started, feature requests, or contributing to the SDK, please reach out to us on [Discord](http://discord.gg/transpose).

### Installation

To install the package, run the following command in your Python environment:

```bash
pip install transpose-decoding-sdk
```

The SDK requires Python 3.6 or higher and has only 4 dependencies:

- [eth-event](https://pypi.org/project/eth-event/)
- [pip-chill](https://pypi.org/project/pip-chill/)
- [web3](https://pypi.org/project/web3/)
- [dateutils](https://pypi.org/project/dateutils/)

## Getting Started

### Load a Contract

The first step in using the SDK is to specify a contract to target. Later, we will stream activity from this contract. To do so, we will import the `TransposeDecodedContract` class and instantiate it with the contract's address, ABI, and chain, as well as a Transpose API key.

In the example below, we specify the contract address for the OpenSea Seaport contract on Ethereum, as well as the path to its ABI (application binary interface):

```python
from transpose.contract import TransposeDecodedContract

contract = TransposeDecodedContract(
    contract_address='0x00000000006c3852cbEf3e08E8dF289169EdE581',
    abi_path='abi/opensea-seaport-abi.json',
    chain='ethereum',
    api_key='YOUR API KEY'
)
```

If you already have the ABI loaded into your Python application, you can pass it directly to the `abi` parameter instead of specifying a path to the ABI file.

### Stream Events

The event streaming routine will stream and decode events emitted by the contract. To use it, simply use the `stream_events` method to generate a new stream. By default, this will start streaming all events in the ABI from the genesis block and will stop once it reaches the latest block. You can consume the stream with an iterator or by calling `next` with the number of events to return:

```python
stream = contract.stream_events()

# read stream with iterator -> returns a single event per loop
for event in stream:
    print(event)

# read stream with `next` -> returns a list of events
print(stream.next(10))
```

#### Block Range

To stream a specific block range, you can specify the `from_block` and `to_block` parameters. The `from_block` parameter is inclusive, while the `to_block` parameter is exclusive. For example, the following code will stream events from block 15M to 16M:

```python
stream = contract.stream_events(
    from_block=16000000,
    to_block=17000000
)
```

You may also specify descending order to stream in the reverse direction. For example, to stream two batches of 10 events in reverse order from the latest block:

```python
stream = contract.stream_events(order='desc')
stream.next(10)
stream.next(10)
```

#### Live Streaming

In order to stream live data, you can specify the `live_stream` parameter. If you use this parameter with a stream iterator, it will continously stream new events as they are added to the blockchain (with a ~3s delay from nodes):

```python
stream = contract.stream_events(
    live_stream=True
)

# continuously iterate over new events
for event in stream:
    print(event)
```

#### Event Filtering

To stream only a specific event, you can specify the `event_name` parameter. You may combine this with the other parameters to further filter by block range and stream the activity live:

```python
stream = contract.stream_events(
    event_name='OrderFulfilled,
    start_block=16000000,
    live_stream=True
)
```

#### Event Format

Each event from the stream will be returned as a dictionary with the same structure, containing `target`, `context`, and `event_data` fields. The `target` field contains information about the contract and event that was decoded, while the `context` field contains information about the block and transaction that the event was emitted in. The `event_data` field contains the decoded event data.

```python
{
    'item': {
        'contract_address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
        'event_name': 'Transfer'
    }, 
    'context': {
        'timestamp': datetime.datetime(2018, 1, 10, 12, 32, 45, tzinfo=datetime.timezone.utc), 
        'block_number': 4885242, 
        'log_index': 35, 
        'transaction_hash': '0x12968bdfc268efaae78a2c1193412ee2d0116a29b85182c7f77a476f6bd2b527', 
        'transaction_position': 197, 
        'confirmed': True
    }, 
    'event_data': {
        'src': '0x004075e4d4b1ce6c48c81cc940e2bad24b489e64', 
        'dst': '0x14fbca95be7e99c15cc2996c6c9d841e54b79425', 
        'wad': 8000000000000000000
    }
}
```

In the example above, the `context.confirmed` field indicates whether the block containing the event has been confirmed by the network.

### Stream Calls

The call streaming routine will stream and decode transactions and traces (a.k.a. internal transactions) to the contract's functions. To use it, simply use the `stream_calls` method to generate a new stream. By default, this will start streaming all calls in the ABI from the genesis block and will stop once it reaches the latest block. You can consume the stream with an iterator or by calling `next` with the number of calls to return:

```python
stream = contract.stream_calls()

# read stream with iterator -> returns a single call per loop
for call in stream:
    print(call)

# read stream with `next` -> returns a list of calls
print(stream.next(10))
```

#### Block Range

To stream a specific block range, you can specify the `from_block` and `to_block` parameters. The `from_block` parameter is inclusive, while the `to_block` parameter is exclusive. For example, the following code will stream calls from block 15M to 16M:

```python
stream = contract.stream_calls(
    from_block=16000000,
    to_block=17000000
)
```

#### Live Streaming

In order to stream live data, you can specify the `live_stream` parameter. If you use this parameter with a stream iterator, it will continously stream new calls as they are added to the blockchain (with a ~3s delay from nodes):

```python
stream = contract.stream_calls(
    live_stream=True
)

# continuously iterate over new calls
for call in stream:
    print(call)
```

#### Call Filtering

To stream only a specific function call, for both transactions and internal transactions, you can specify the `function_name` parameter. You may combine this with the other parameters to further filter by block range and stream the activity live:

```python
stream = contract.stream_calls(
    function_name='transfer',
    start_block=16000000,
    live_stream=True
)
```

You may also specify descending order to stream in the reverse direction. For example, to stream two batches of 10 calls in reverse order from the latest block:

```python
stream = contract.stream_calls(order='desc')
stream.next(10)
stream.next(10)
```

#### Call Format

Each call from the stream will be returned as a dictionary with the same structure, containing `target`, `context`, `call_data`, `input_data`, and `output_data` fields. The `target` field contains information about the contract and function that was decoded, while the `context` field contains information about the block, transaction, and trace that the call was made in. The `call_data` field contains the decoded call data, while the `input_data` and `output_data` fields contain the decoded input and output data, respectively.

```python
{
    'item': {
        'contract_address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
        'function_name': 'withdraw'
    }, 
    'context': {
        'timestamp': datetime.datetime(2022, 6, 21, 2, 28, 20, tzinfo=datetime.timezone.utc), 
        'block_number': 15000000, 
        'transaction_hash': '0x3b5abcc2e67901638b944f5db15f5b13231b5392a6d6c4115407d9106136ac2f', 
        'transaction_position': 5, 
        'trace_index': 5, 
        'trace_address': [0, 2, 0], 
        'trace_type': 'call', 
        'confirmed': True
    }, 
    'call_data': {
        'type': 'internal_transaction', 
        'from_address': '0x2339d36BCe71c97772e54C76fF6b4C74C9DD8f86', 
        'to_address': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 
        'eth_value': 0
    }, 
    'input_data': {
        'wad': 6640125949176909399
    },
    'output_data': {}
}
```

In the example above, the `context.confirmed` field indicates whether the block containing the event has been confirmed by the network. Additionally, the `call.type` field will either be set to `transaction` or `internal_transaction` depending on whether the call was a transaction or trace, respectively. If the call was a transaction, the `trace_index` will be zero, the `trace_address` will be an empty list, and the `trace_type` will be `call`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Citations

If you use this library in your research, please cite it as:

```bibtex
@misc{transpose-decoding-sdk,
  author = {Alex Langshur},
  title = {Transpose Decoding SDK},
  year = {2022},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/TransposeData/transpose-decoding-sdk}},
  commit = {64dc9c870df4326b07009876cdfdf749e882d191}
}
```
