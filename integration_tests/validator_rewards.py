from terra_sdk.client.lcd import LCDClient

terra = LCDClient(
    chain_id="secret-4",
    url="https://secret-4--lcd--full.datahub.figment.io/apikey/528a747ecdb5c88f843eaa9e8e59dce5/",)
print(terra.distribution.validator_rewards("secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7"))

