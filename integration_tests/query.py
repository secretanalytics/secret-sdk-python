from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id


def main():
    secret = LocalSecret(chain_id=main_net_chain_id)

    result = secret.bank.balance(
        address="secret19y0n2ru9dae9w6vt7fwgfptp5nxq3hwtsz4u75"
    )
    print(result)


main()
