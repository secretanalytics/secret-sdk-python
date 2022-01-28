from secret_sdk.client.localsecret import (
    LOCAL_MNEMONICS,
    LocalSecret,
    test_net_chain_id,
)
from secret_sdk.core import Coins

secret = LocalSecret(chain_id=test_net_chain_id)
test1 = secret.wallets["test1"]

print(test1)

result = test1.send_tokens(
    test1.key.acc_address,
    LOCAL_MNEMONICS[test_net_chain_id]["test2"]["address"],
    Coins.from_str("1000000uscrt"),
    gas=250_000,
)
print(result)
