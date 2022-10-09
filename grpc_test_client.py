import os
import asyncio

from secret_sdk.client.grpc.grpc_client import AsyncGRPCClient


async def run():
    host = os.environ.get("SN_API")
    port = '9090'
    client = AsyncGRPCClient(host=host, port=port)

    # Compute
    address = "secret1k0jntykt7e4g3y88ltc60czgjuqdy4c9e8fzek"
    query = '{"token_info":{}}'
    code_id = 5

    contract_code_hash = await client.query.secret.compute.contract_code_hash(address)
    print(contract_code_hash)

    code_hash = await client.query.secret.compute.code_hash(code_id)
    print(code_hash)

    contract_info = await client.query.secret.compute.contract_info(address)
    print(contract_info)

    try:
        contracts_by_code = await client.query.secret.compute.contracts_by_code(code_id)
        print(contracts_by_code)
    except NotImplementedError:
        pass

    code = await client.query.secret.compute.code(code_id)
    print(code)

    codes = await client.query.secret.compute.codes()
    print(codes)

    query_contract = await client.query.secret.compute.query_contract(
        contract_address=address, query=query
    )
    print(query_contract)

    query_contract = await client.query.secret.compute.query_contract(
        contract_address=address, query=query, code_hash=code_hash
    )
    print(query_contract)

    # Get Tx
    tx = await client.get_tx(
        hash="8A7AB522A831A5EB4B3840BAF5429B0BA41BB5BEDE48066C055114D721BCEF36"
    )
    print(tx)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
