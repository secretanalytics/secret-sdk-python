LCDClient
=========

The :class:`LCDClient` is an object representing a HTTP connection to a Secret LCD node.

Get connected
-------------

Create a new LCDClient instance by specifying the URL and chain ID of the node to connect to.

.. note::
    It is common practice to name the active LCDClient instance ``secret``, but this is not required.

.. code-block:: python

    >>> from secret_sdk.client.lcd import LCDClient
    >>> secret = LCDClient(url="https://api.scrt.network", chain_id="secret-4")
    >>> secret.tendermint.node_info()['node_info']['network']
    'secret-4'

You can also specify gas estimation parameters for your chain for building transactions.

.. code-block:: python
    :emphasize-lines: 8-9

    import requests
    from secret_sdk.core import Coins

    secret = LCDClient(
        url="https://api.scrt.network",
        chain_id="secret-4",
        gas_prices=Coins({"uscrt": 0.25}),
        gas_adjustment="1.4"
    )    


Using the module APIs
---------------------

LCDClient includes functions for interacting with each of the core modules (see sidebar). These functions are divided and
and organized by module name (eg. :class:`secret.market<secret_sdk.client.lcd.api.market.MarketAPI>`), and handle
the tedium of building HTTP requests, parsing the results, and handling errors. 

Each request fetches live data from the blockchain:

.. code-block:: python

    >>> secret.market.parameters()
    {'base_pool': '7000000000000.000000000000000000', 'pool_recovery_period': '200', 'min_spread': '0.005000000000000000'}

The height of the last result (if applicable) is available:

.. code-block:: python

    >>> secret.last_request_height
    89292


Create a wallet
---------------

LCDClient can create a :class:`Wallet` object from any :class:`Key` implementation. Wallet objects
are useful for easily creating and signing transactions.

.. code-block:: python

    >>> from secret_sdk.key.mnemonic import MnemonicKey
    >>> mk = MnemonicKey()
    >>> wallet = secret.wallet(mk)
    >>> wallet.account_number()
    27


LCDClient Reference
-------------------

.. autoclass:: secret_sdk.client.lcd.LCDClient
    :members: