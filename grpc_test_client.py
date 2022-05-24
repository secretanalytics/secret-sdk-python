from secret_sdk.client.grpc.grpcclient import AsyncGRPCClient
import asyncio
from secret_sdk.client.grpc.encryption import EncryptionUtils


async def run():
    host = "scrt-validator.digiline.io"
    port = "9090"
    eu = EncryptionUtils(host=host, port=port)
    client = AsyncGRPCClient(host=host, port=port)
    address = "secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek"
    # address = "secret1wkcgkmnnz3jhp7vf76jfypqrvqq2jjfnsde3df"
    query = '{"token_info":{}}'
    # print(
    #     (
    #         await client.query.secret.compute.query_contract(
    #             contract_address=address, query=query
    #         )
    #     )
    # )

    print(
        (
            await client.txService.get_tx(
                hash="2681602DF1D4942005BA6517934D6AA467ED9DE63CF36E77E7C8439D4A78E45F"
            )
        )
    )
    # print(await client.query.secret.original_compute.contract_info(address=b))
    # query_hash = await eu.encrypt(address_hash, '{"pool": {}}')
    # print(query_hash)
    # print((await client.secret.compute.smart_contract_state(address=address_hash, query_data=query_hash)).to_json)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
