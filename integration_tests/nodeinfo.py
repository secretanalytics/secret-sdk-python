from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id

secret = LocalSecret(chain_id=main_net_chain_id)
res = secret.tendermint.node_info()
print(res)
