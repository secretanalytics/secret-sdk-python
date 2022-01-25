from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id


api = LocalSecret(chain_id=main_net_chain_id)
validators_with_voting_power = api.utils.validators_with_voting_power()
print(validators_with_voting_power)
