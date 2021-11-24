from secret_sdk.client.lcd import LCDClient
from integration_tests.config import api_url

terra = LCDClient(
    chain_id="secret-4",
    url=api_url)
print(terra.distribution.validator_rewards("secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7"))

