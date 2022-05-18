from audioop import add
from secret_sdk.client.grpc.grpcclient import AsyncGRPCClient
import asyncio
import bech32
import base64
from secret_sdk.client.grpc.encryption import EncryptionUtils


async def run():

    eu = EncryptionUtils(host="172.241.26.28", port="9090")
    client = AsyncGRPCClient(host="172.241.26.28", port="9090")
    address = b"secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek"
    query = '{"pool": {}}'
    print(await client.reflection.list_all_interfaces())

    # query_hash = await eu.encrypt(address_hash, '{"pool": {}}')
    # print(query_hash)
    # print((await client.secret.compute.smart_contract_state(address=address_hash, query_data=query_hash)).to_json)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
