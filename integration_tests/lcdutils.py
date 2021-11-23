from terra_sdk.client.lcd import LCDClient

api = LCDClient(chain_id="secret-4", url="https://secret-4--lcd--full.datahub.figment.io/apikey/528a747ecdb5c88f843eaa9e8e59dce5/")
validators_with_voting_power = api.utils.validators_with_voting_power()
print(validators_with_voting_power)

