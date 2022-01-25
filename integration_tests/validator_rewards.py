from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id


secret = LocalSecret(chain_id=main_net_chain_id)
print(secret.distribution.validator_rewards("secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7"))

