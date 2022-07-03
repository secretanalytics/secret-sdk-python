from secret_sdk.client.grpc.grpc_client import AsyncGRPCClient
import asyncio

import os


async def run():
    host = os.environ.get("SN_API")
    port = "9090"
    client = AsyncGRPCClient(host=host, port=port)
    address = "secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek"
    # address = "secret1wkcgkmnnz3jhp7vf76jfypqrvqq2jjfnsde3df"
    query = '{"token_info":{}}'
    print(
        (
            await client.query.secret.compute.query_contract(
                contract_address=address, query=query
            )
        )
    )

    tx = await client.get_tx(
        hash="81818C55B5FBE9C36C2F92D5E2395B3EBD0853C7632D2C1A24740C30FE88CD81"
    )

    print(f"\nafter_{tx}\n")

    # print(await client.query.secret.original_compute.contract_info(address=b))
    # query_hash = await eu.encrypt(address_hash, '{"pool": {}}')
    # print(query_hash)
    # print((await client.secret.compute.smart_contract_state(address=address_hash, query_data=query_hash)).to_json)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
