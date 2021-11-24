from secret_sdk.client.lcd import LCDClient
from integration_tests.config import api_url

secret = LCDClient(
    chain_id="secret-4",
    url = api_url,
)
res = secret.tendermint.node_info()
print(res)
