from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id

secret = LocalSecret(chain_id=main_net_chain_id)

res = secret.auth.account_info(address="secret19y0n2ru9dae9w6vt7fwgfptp5nxq3hwtsz4u75")
print(res)

res = secret.auth.account_info(address="secret1c7rjffp9clkvrzul20yy60yhy6arnv7sde0kjj")
print(res)
