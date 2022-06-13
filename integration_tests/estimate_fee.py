from secret_sdk.core import Coins
from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id

api = LocalSecret(chain_id=main_net_chain_id)
fee = api.tx.estimate_fee(gas=250_000)
print(fee)

fee = api.tx.estimate_fee(
    gas=200_000, gas_prices=Coins.from_data([{"amount": 0.25, "denom": "uscrt"}])
)
print(fee)

fee = api.tx.estimate_fee(
    gas=200_000,
    gas_prices=Coins.from_data([{"amount": 0.25, "denom": "uscrt"}]),
    gas_adjustment=1.2,
    fee_denoms=["uscrt"],
)
print(fee)

fee = api.tx.estimate_fee(
    gas=200_000,
    gas_prices=Coins.from_data([{"amount": 0.25, "denom": "uscrt"}]),
    fee_denoms=["ukrw"],
)
print(fee)
