from secret_sdk.core import Coins
from secret_sdk.client.lcd.api.tx import CreateTxOptions
from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id

options_to_test =[
    CreateTxOptions(msgs=[], gas='250000'),
    CreateTxOptions(msgs=[], gas='200000', gas_prices=Coins('0.25uscrt')),
    CreateTxOptions(msgs=[], gas='200000', gas_prices=Coins('0.25uscrt'), gas_adjustment=1.2),
    CreateTxOptions(msgs=[], gas='200000', gas_prices=Coins('0.25uscrt'), fee_denoms=['ukrw']) # return nothing

]
api = LocalSecret(chain_id=main_net_chain_id)
for opt in options_to_test:
    fee = api.tx.estimate_fee(
        opt
    )
    print(fee)
