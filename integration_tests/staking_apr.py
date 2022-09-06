from secret_sdk.client.localsecret import LocalSecret, main_net_chain_id


def main():
    secret_client = LocalSecret(
        chain_id=main_net_chain_id,
    )

    network_inflation = 0.150   # 15%

    pool_result = secret_client.staking.pool()
    bonded = pool_result.bonded_tokens.amount / 10**6

    community_result = secret_client.distribution.community_pool()
    community_amount = community_result.get("uscrt").amount / 10**6

    supply_result = secret_client.bank.total_denom("uscrt")
    supply = supply_result.amount / 10**6

    ratio = bonded / (supply - community_amount)
    staking_apr = float(network_inflation / ratio)
    print("staking_apr: ", staking_apr)


main()