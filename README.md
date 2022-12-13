# transpose-decoding-sdk

The Transpose Decoding SDK is a Python package that makes decoding contract activity on EVM blockchains as simple as possible. Simply specify a contract address and ABI to start streaming historical or live activity across decoded logs, transactions, and traces.

## Features

- **Simple interface**: Simple, minimal code interface to stream decoded events or calls.
- **High performance**: Streaming benchmarked at 3,000+ items per second.
- **Automatic decoding**: Automatically decode inputs/outputs for transactions and traces, and logs for events.
- **Live & historical**: Stream activity in a historical block range or live with a ~3s delay from nodes.
- **Full traces support**: Decode traces (a.k.a. internal transactions) just like transactions.
- **Multi-chain**: Supports Ethereum, Polygon, and Goerli with additional chains coming soon.
- **Event & function filtering**: Stream all events/calls in an ABI or target a specific event or function name.

## Setup

### Retrieving an API key

To use the SDK, you will need an API key for Transpose. You can sign up for a free API key by visting the [Transpose App](https://app.transpose.io). If you have any questions on getting started, feature requests, or contributing to the SDK, please reach out to us on [Discord](http://discord.gg/transpose).

### Installation

To install the package, run the following command in your Python environment:

```bash
pip install transpose-decoding-sdk
```

The SDK requires Python 3.6 or higher and has only 3 dependencies:

- `eth-event`
- `pip-chill`
- `web3`

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

### Streaming Events

To stream events, simply use the `stream_events` methods to generate a new stream. By default, this will start streaming all events in the ABI from the genesis block and will stop once it reaches the latest block. You can consume the stream activity with an iterator or by calling `next` on the stream with the number of items to return:

```python
stream = contract.stream_events()

# read stream with iterator
for event in stream:
    print(event)

# read stream with `next`
print(stream.next(10))
```

To stream a specific block range, you can specify the `from_block` and `to_block` parameters. The `from_block` parameter is inclusive, while the `to_block` parameter is exclusive. For example, the following code will stream events from block 15M to 16M:

```python
stream = contract.stream_events(
    from_block=16000000,
    to_block=17000000
)
```

To stream only a specific event, you can specify the `event_name` parameter:

```python
stream = contract.stream_events(
    event_name='OrderFulfilled
)
```
