from terra_sdk.client.localterra import LocalTerra
from terra_sdk.core import Coins
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank.msgs import MsgSend

def main():
    terra = LocalTerra()
    test1 = terra.wallets["test1"]

    gas = 300_000
    gas_price = 0.25
    fee = StdFee(gas, Coins.from_data([{"amount": int(gas * gas_price), "denom": "uscrt"}]))

    # test net addresses
    send_msg = MsgSend("secret1ljtckgv3gsgrnhf7f3ygquyse5urwkamx7ln27", "secret16a7hp3wr4esccstuat4syavv6ylpzpd4kn0jp9",
                       Coins.from_str("5000000uscrt"))
    tx = test1.create_and_sign_tx([send_msg], fee=fee)
    send_scrt_tx = terra.tx.broadcast(tx)
    print('send scrt:\n', send_scrt_tx)
    # pool query
    pool_query = terra.wasm.contract_query('secret16krcdrqh6y6pazvkj58nrvkerk0q0ttg22kepl', {"pool": {}})
    print('pool query scrt/sscrt:\n', pool_query)

    # convert scrt / sscrt
    addr = test1.key.acc_address
    execute_msg = terra.wasm.contract_execute_msg(addr, 'secret1s7c6xp9wltthk5r6mmavql4xld5me3g37guhsx', {'deposit': {}},
                                              Coins.from_str('1000000uscrt'))

    convert_scrt_sscrt = test1.create_and_sign_tx([execute_msg], fee=fee)
    convert_scrt_sscrt_tx = terra.tx.broadcast(convert_scrt_sscrt)
    print('convert scrt/sscrt:\n',convert_scrt_sscrt_tx)
main()
