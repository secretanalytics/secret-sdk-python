from terra_sdk.client.lcd import LCDClient

api = LCDClient(chain_id="holodeck-2", url="https://bootstrap.secrettestnet.io")
validators_with_voting_power = api.utils.validators_with_voting_power()
print(validators_with_voting_power)
tax = api.utils.calculate_tax("100000000uscrt")
print(tax)
