from integration_tests.config import api_url
from secret_sdk.client.lcd import LCDClient
from secret_sdk.util.contract import get_contract_events

api = LCDClient(url=api_url, chain_id="secret-4")
tx_info = api.tx.tx_info(
    "9F90D988CE4569CAB07AC0331E188AD873FCAAA21B9701FB8705AE6053620C72"
)
print(get_contract_events(tx_info))
