from terra_sdk.client.lcd import LCDClient
from terra_sdk.util.contract import get_contract_events

api = LCDClient(url="https://secret-4--lcd--full.datahub.figment.io/apikey/528a747ecdb5c88f843eaa9e8e59dce5/", chain_id="secret-4")
tx_info = api.tx.tx_info(
    "9F90D988CE4569CAB07AC0331E188AD873FCAAA21B9701FB8705AE6053620C72"
)
print(get_contract_events(tx_info))
