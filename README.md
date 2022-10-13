# <div  align="center"> <p > Python SDK for Secret Network </p>

<br>
<br>
The Secret Software Development Kit (SDK) in Python is a simple library toolkit for building software that can interact with the Secret blockchain and provides simple abstractions over core data structures, serialization, key management, and API request generation. The SDK is based on a fork of <a href="https://github.com/terra-money/terra.py">terra.py</a> on Terra 

## Features

- Written in Python offering extensive support libraries
- Versatile support for key management solutions
- Exposes the Secret Rest API through LCDClient

<br/>

# Table of Contents
- [API Reference](#api-reference)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Dependencies](#dependencies)
  - [Tests](#tests)
  - [Code Quality](#code-quality)
- [Usage Examples](#usage-examples) 
  - [Getting Blockchain Information](#getting-blockchain-information)
    - [Async Usage](#async-usage)
  - [Building and Signing Transactions](#building-and-signing-transactions)
      - [Example Using a Wallet](#example-using-a-wallet-recommended)
- [Contributing](#contributing)
  - [Reporting an Issue](#reporting-an-issue)
  - [Requesting a Feature](#requesting-a-feature)
  - [Contributing Code](#contributing-code)
  - [Documentation Contributions](#documentation-contributions)
- [License](#license)

<br/>



# API Reference
An intricate reference to the APIs on the Secret SDK can be found <a href="https://api.scrt.network/swagger/">here</a>.

<br/>

# Getting Started
A walk-through of the steps to get started with the Secret SDK alongside with a few use case examples are provided below. 

## Requirements
Secret SDK requires <a href="https://www.python.org/downloads/">Python v3.7+</a>.

## Installation

<sub>**NOTE:** *All code starting with a `$` is meant to run on your terminal (a bash prompt). All code starting with a `>>>` is meant to run in a python interpreter, like <a href="https://pypi.org/project/ipython/">ipython</a>.*</sub>

Secret SDK can be installed (preferably in a `virtual environment` from PyPI using `pip`) as follows:

```
$ pip install -U secret-sdk
```
<sub>*You might have `pip3` installed instead of `pip`; proceed according to your own setup.*<sub>

## Dependencies
Secret SDK uses <a href="https://python-poetry.org/">Poetry</a> to manage dependencies. To get set up with all the required dependencies, run:
```
$ pip install poetry
$ poetry install
```


## Tests
Secret SDK provides extensive tests for data classes and functions. To run them, after the steps in [Dependencies](#dependencies):
```
$ make test
```

<br/>

# Usage Examples
Secret SDK can help you read block data, query secret contracts, sign and send transactions, and many more.
Following examples are provided to help get building started.

In order to interact with the Secret blockchain, you'll need a connection to a Secret node or an api. This can be done through setting up an LCDClient (The LCDClient is an object representing an HTTP connection to a Secret LCD node.):

```
>>> from secret_sdk.client.lcd import LCDClient
>>> secret = LCDClient(chain_id="secret-4", url=node_rest_endpoint)
```

## Getting Blockchain Information

Once properly configured, the `LCDClient` instance will allow you to interact with the Secret blockchain. Try getting the latest block height:


```
>>> secret.tendermint.block_info()['block']['header']['height']
```

`'1687543'`


### Async Usage

If you want to make asynchronous, non-blocking LCD requests, you can use AsyncLCDClient. The interface is similar to LCDClient, except the module and wallet API functions must be awaited.


<pre><code>
>>> import asyncio 
>>> from secret_sdk.client.lcd import AsyncLCDClient

>>> async def main():
        <strong>async with AsyncLCDClient(url=node_rest_endpoint, chain_id="secret-4") as secret:</strong>
            community_pool = await secret.distribution.community_pool()
            print(community_pool)
            <strong>await secret.session.close()  # you must close the session</strong>

>>> asyncio.get_event_loop().run_until_complete(main())
</code></pre>

You can improve the efficiency of consecutive queries by making them asynchronous.

<pre><code>
>>> import asyncio
>>> import uvloop

>>> from secret_sdk.client.lcd import AsyncLCDClient
>>> from secret_sdk.exceptions import LCDResponseError

>>> def owner_of(token_id):
        return {
                "owner_of": {
                    "token_id": token_id,
                }
            }

>>> async def query_owner(secret, contract_address, token_id, query):
        try:
            msg = await secret.wasm.contract_query(contract_address, query)
            return (token_id, msg["owner_of"]["owner"])
        except LCDResponseError:
            return (token_id, "")

>>> async def query_collection(contract_address, token_ids):
        <strong>async with AsyncLCDClient(chain_id="secret-4", url=node_rest_endpoint) as secret: </strong>
            requests = [query_owner(secret, contract_address, token, owner_of(token)) for token in token_ids]
            <strong>owners = await asyncio.gather(*requests, return_exceptions=True)</strong>
            print(owners)
            <strong>await secret.session.close() # you must close the session </strong>

>>> uvloop.install()
>>> if __name__ == '__main__':
        asyncio.run(query_collection(contract_address, token_ids))
</code></pre>

## Building and Signing Transactions

If you wish to perform a state-changing operation on the Secret blockchain such as sending tokens, swapping assets, withdrawing rewards, or even invoking functions on smart contracts, you must create a **transaction** and broadcast it to the network.
Secret SDK provides functions that help create StdTx objects.

### Example Using a Wallet (*recommended*)

A `Wallet` allows you to create and sign a transaction in a single step by automatically fetching the latest information from the blockchain (chain ID, account number, sequence).

Use `LCDClient.wallet()` to create a Wallet from any Key instance. The Key provided should correspond to the account you intend to sign the transaction with.


```
>>> from secret_sdk.client.lcd import LCDClient
>>> from secret_sdk.key.mnemonic import MnemonicKey

>>> mk = MnemonicKey(mnemonic=MNEMONIC) 
>>> secret = LCDClient(node_rest_endpoint, "secret-4")
>>> wallet = secret.wallet(mk)
```

Once you have your Wallet, you can create a StdTx using `Wallet.create_and_sign_tx` then broadcast it to the network with `secret.tx.broadcast` with your broadcast mode of choice (block, sync, async - see cosmos docs).

```
>>> from secret_sdk.core.auth import StdFee
>>> from secret_sdk.core.bank import MsgSend

>>> send_msg = MsgSend(
            wallet.key.acc_address,
            RECIPIENT,
            "1000000uscrt"    # send 1 scrt
        )
>>> tx = wallet.create_and_sign_tx(
        msgs=[send_msg],
        memo="My first transaction!",
        fee=StdFee(200000, "120000uscrt")
    )
>>> result = secret.tx.broadcast(tx)
>>> print(result)
```

Or use the abstraction `wallet.send_tokens` (see `wallet.execute_tx` to execute a smart contract with `handle_msg`).

```
>>> tx = wallet.send_tokens(recipient_addr=RECIPIENT, transfer_amount="1000000uscrt")
```

### Batch Transactions
You can combine muliple state-changing transactions for the same contract into a single transaction. The contract used here is from the [Counter contract example](https://docs.scrt.network/secret-network-documentation/development/intro-to-secret-contracts)

```
msg = {
  'increment': {}
}

msg_list = [msg for _ in range(10)]

tx = wallet.execute_tx(
  CONTRACT_ADDR,
  msg_list,
  memo="My first batch transaction!",
)
```

<br/>

# Contributing

Community contribution, whether it's a new feature, correction, bug report, additional documentation, or any other feedback is always welcome. Please read through this section to ensure that your contribution is in the most suitable format for us to effectively process.

<br/>

## Reporting an Issue 
First things first: **Do NOT report security vulnerabilities in public issues!** Please disclose responsibly by letting the Secret SDK team know upfront (discord , telegram). We will assess the issue as soon as possible on a best-effort basis and will give you an estimate for when we have a fix and release available for an eventual public disclosure. </br>
If you encounter a different issue with the Python SDK, check first to see if there is an existing issue on the Issues page or a pull request on the Pull request page (both Open and Closed tabs) addressing the topic.

If there isn't a discussion on the topic there, you can file an issue. The ideal report includes:

* A description of the problem / suggestion.
* How to recreate the bug.
* If relevant, including the versions of your:
    * Python interpreter
    * Secret SDK
    * Optionally of the other dependencies involved
* If possible, create a pull request with a (failing) test case demonstrating what's wrong. This makes the process for fixing bugs quicker & gets issues resolved sooner.
</br>

## Requesting a Feature
If you wish to request the addition of a feature, please first checkout the Issues page and the Pull requests page (both Open and Closed tabs). If you decide to continue with the request, think of the merits of the feature to convince the project's developers, and provide as much detail and context as possible in the form of filing an issue on the Issues page.


<br/>

## Contributing Code
If you wish to contribute to the repository in the form of patches, improvements, new features, etc., first scale the contribution. If it is a major development, like implementing a feature, it is recommended that you consult with the developers of the project before starting the development in order not to risk spending a lot of time working on a change that might not get merged into the project. Once confirmed, you are welcome to submit your pull request.
</br>

### For new contributors, here is a quick guide: 

1. Fork the repository.
2. Build the project using the [Dependencies](#dependencies) and [Tests](#tests) steps.
3. Install a <a href="https://virtualenv.pypa.io/en/latest/index.html">virtualenv</a>.
4. Develop your code and test the changes using the [Tests](#tests) and [Code Quality](#code-quality) steps.
5. Commit your changes
6. Push your fork and submit a pull request to the repository's `main` branch to propose your code.
   

A good pull request:
* is clear.
* works across all supported versions of Python. (3.7+)
* Follows the existing style of the code base (<a href="https://pypi.org/project/flake8/">`Flake8`</a>).
* Has comments included as needed.
* A test case that demonstrates the previous flaw that now passes with the included patch, or demonstrates the newly added feature.
* If it adds / changes a public API, it must also include documentation for those changes.
* Must be appropriately licensed (MIT License).
</br>

## Documentation Contributions
Documentation improvements are always welcome. The documentation files live in the [docs](./docs) directory of the repository and are written in <a href="https://docutils.sourceforge.io/rst.html">reStructuredText</a> and use <a href="https://www.sphinx-doc.org/en/master/">Sphinx</a> to create the full suite of documentation.
</br>
When contributing documentation, please do your best to follow the style of the documentation files. This means a soft-limit of 88 characters wide in your text files and a semi-formal, yet friendly and approachable, prose style. You can propose your imporvements by submiting a pull request as explained above.

### Need more information on how to contribute?
You can give this <a href="https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution">guide</a> read for more insight.


<br/>

# License

This software is licensed under the MIT license. See [LICENSE](./LICENSE) for full disclosure.


