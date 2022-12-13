# transpose-decoding-sdk

The Transpose Decoding SDK is a Python package that makes decoding contract activity on EVM blockchains as simple as possible. Simply specify a contract address and ABI to start streaming historical or live acitivty across decoded events, transactions, and traces.

## Introduction

In general, contract activity includes both events emitted by the contract and calls to the contract's functions (transactions and traces). There exist several major problems when it comes to decoding and streaming this activity:

1. Using the RPC API (the current approach) is very slow and complex.
2. There is no way to bulk stream historical activity.
3. No availability for filtering transactions by contract and function.
4. No support for traces (a.k.a. internal transactions) whatsoever.
5. No automated decoding of transaction/traces inputs and outputs.

The SDK provides a very simple interface to stream this decoded activity historically and live using just a contract address, ABI, and Transpose API key.

## Retrieving an API key

To use the SDK, you will need an API key for Transpose. You can sign up for a free API key by visting the [Transpose App](https://app.transpose.io). If you have any questions on getting started, feature requests, or contributing to the SDK, please reach out to us on [Discord](http://discord.gg/transpose).

## Installation

To install the package, run the following command in your Python environment:

```bash
pip install transpose-decoding-sdk
```

The SDK requires Python 3.6 or higher and has only 3 dependencies:

- `eth-event`
- `pip-chill`
- `web3`
