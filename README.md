# transpose-decoding-sdk

The Transpose Decoding SDK is a Python package that makes decoding contract activity on EVM blockchains as simple as possible. Simply specify a contract address and ABI to start streaming historical or live acitivty across decoded events, transactions, and traces.

## Features

- **Simple interface**: Simple, minimal code interface to stream decoded events or calls.
- **High performance**: Streaming benchmarked at 3,000+ items per second.
- **Live and historical**: Stream decoded activity between historical block ranges or live with a ~3s delay from nodes.
- **Automatic decoding**: Automatically decode inputs/outputs for transactions and traces, and logs for events.
- **Full traces support**: Decode traces (a.k.a. internal transactions) just like transactions in the correct order.
- **Multi-chain**: Supports Ethereum, Polygon, and Goerli with additional chains coming soon.
- **Function and event filtering**: Stream all events or functions in an ABI or specify a specific event or function name.

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

### Streaming Events

