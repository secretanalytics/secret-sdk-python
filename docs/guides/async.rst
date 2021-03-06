Usage with asyncio
==================
    
If you want to make asynchronous, non-blocking LCD requests, you can use AsyncLCDClient.
The interface is similar to LCDClient, except the module and wallet API functions must be awaited.

Async module APIs
-----------------

You can replace your LCDClient instance with AsyncLCDClient inside a coroutine function:

.. code-block:: python
    :emphasize-lines: 5,8

    import asyncio 
    from secret_sdk.client.lcd import AsyncLCDClient

    async def main():
        secret = AsyncLCDClient("https://api.scrt.network", "secret-4")
        total_supply = await secret.supply.total()
        print(total_supply)
        await secret.session.close() # you must close the session

    asyncio.get_event_loop().run_until_complete(main())


For convenience, you can use the async context manager to automatically teardown the
session. Here's the same code as above, this time using the ``async with`` construct.

.. code-block:: python
    :emphasize-lines: 5

    import asyncio 
    from secret_sdk.client.lcd import AsyncLCDClient

    async def main():
        async with AsyncLCDClient("https://api.scrt.network", "secret-4") as secret:
            total_supply = await secret.supply.total()
            print(total_supply)

    asyncio.get_event_loop().run_until_complete(main())

Async wallet API
----------------

When creating a wallet with AsyncLCDClient, the wallet's methods that create LCD requests
are also asychronous and therefore must be awaited.

.. code-block:: python
    :emphasize-lines: 12-13

    import asyncio 
    from secret_sdk.client.lcd import AsyncLCDClient
    from secret_sdk.key.mnemonic import MnemonicKey
    from secret_sdk.core import Coins

    mk = MnemonicKey()
    recipient = "secret1..."

    async def main():
        async with AsyncLCDClient("https://api.scrt.network", "secret-4") as secret:
            wallet = secret.wallet(mk)
            account_number = await wallet.account_number()
            tx = await wallet.create_and_sign_tx(
                msgs=[MsgSend(wallet.key.acc_address, recipient, Coins(uscrt=10202))]
            )
    
    asyncio.get_event_loop().run_until_complete(main())

Alternative event loops
-----------------------

The native ``asyncio`` event loop can be replaced with an alternative such as ``uvloop``
for more performance. For example:

.. code-block:: python
    :emphasize-lines: 2, 10

    import asyncio
    import uvloop

    from secret_sdk.client.lcd import AsyncLCDClient

    async def main():
        async with AsyncLCDClient("https://api.scrt.network", "secret-4") as secret:
            total_supply = await wallet.supply.total()

    uvloop.install() 
    asyncio.get_event_loop().run_until_complete(main())