from secret_sdk.client.lcd import LCDClient
from integration_tests.config import api_url

api = LCDClient(chain_id="secret-4", url=api_url)
validators_with_voting_power = api.utils.validators_with_voting_power()
print(validators_with_voting_power)
