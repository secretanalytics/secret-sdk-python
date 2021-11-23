from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    chain_id="secret-4",
    url="https://secret-4--lcd--full.datahub.figment.io/apikey/528a747ecdb5c88f843eaa9e8e59dce5/",
)
res = terra.tendermint.node_info()
print(res)
