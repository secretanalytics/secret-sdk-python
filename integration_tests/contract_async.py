import asyncio

from secret_sdk.client.localsecret import AsyncLocalSecret
from secret_sdk.core import Coins
from secret_sdk.core.auth import StdFee
from secret_sdk.core.bank.msgs import MsgSend


async def async_main():
    gas = 300_000
    gas_price = 0.25
    fee = StdFee(gas, Coins.from_data([{"amount": int(gas * gas_price), "denom": "uscrt"}]))

    async with AsyncLocalSecret() as secret:
        test1 = secret.wallets["test1"]

        # test net addresses
        send_msg = MsgSend("secret1ljtckgv3gsgrnhf7f3ygquyse5urwkamx7ln27", "secret16a7hp3wr4esccstuat4syavv6ylpzpd4kn0jp9",
                           Coins(uscrt = 5000000))
        tx = await test1.create_and_sign_tx([send_msg], fee=fee)
        send_scrt_tx = await secret.tx.broadcast(tx)
        print('send scrt:\n', send_scrt_tx)
        # pool query
        pool_query = await secret.wasm.contract_query('secret16krcdrqh6y6pazvkj58nrvkerk0q0ttg22kepl', {"pool": {}})
        print('pool query scrt/sscrt:\n', pool_query)

        # convert scrt / sscrt
        addr = test1.key.acc_address
        execute_msg = await secret.wasm.contract_execute_msg(addr, 'secret1s7c6xp9wltthk5r6mmavql4xld5me3g37guhsx',
                                                      {'deposit': {}},
                                                      Coins(uscrt = 1000000))

        convert_scrt_sscrt = await test1.create_and_sign_tx([execute_msg], fee=fee)
        convert_scrt_sscrt_tx = await secret.tx.broadcast(convert_scrt_sscrt)
        print('convert scrt/sscrt:\n', convert_scrt_sscrt_tx)



loop = asyncio.new_event_loop()
loop.run_until_complete(async_main())
