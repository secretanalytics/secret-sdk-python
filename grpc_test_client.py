from audioop import add
import base64

from secret_sdk.client.grpc.grpcclient import AsyncGRPCClient
import asyncio
from secret_sdk.client.grpc.encryption import EncryptionUtils
from secret_sdk.client.grpc.query.compute import ComputeQuerier


async def run():
    host = "scrt-validator.digiline.io"
    port = "9090"
    eu = EncryptionUtils(host=host, port=port)
    client = AsyncGRPCClient(host=host, port=port)
    print((await client.query.auth.params()).to_dict())
    address = "secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek"
    query = '{"pool": {}}'
    b = ComputeQuerier.address_to_bytes(address)

    print(f"{address} -> {b}")
    res_address = ComputeQuerier.bytes_to_address(b)
    print(f"{b} -> {res_address}")

    # result = (await client.query.auth.accounts()).to_dict()

    print(
        await client.query.secret.original_compute.contract_info(address=b)
    )  # .query_contract(address, query))

    # query_hash = await eu.encrypt(address_hash, '{"pool": {}}')
    # print(query_hash)
    # print((await client.secret.compute.smart_contract_state(address=address_hash, query_data=query_hash)).to_json)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
