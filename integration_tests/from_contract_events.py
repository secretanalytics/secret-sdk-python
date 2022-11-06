from secret_sdk.util.contract import get_contract_events

from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id

secret = LocalSecret(chain_id=main_net_chain_id)
tx_info = secret.tx.tx_info(
    "9F90D988CE4569CAB07AC0331E188AD873FCAAA21B9701FB8705AE6053620C72"
)
print(get_contract_events(tx_info))
