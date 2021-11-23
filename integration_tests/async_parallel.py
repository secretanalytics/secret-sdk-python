import asyncio

import uvloop

from terra_sdk.client.lcd import AsyncLCDClient


async def with_sem(aw, sem):
    async with sem:
        print(sem)
        return await aw


async def main():
    api = AsyncLCDClient(url="https://secret-4--lcd--full.datahub.figment.io/apikey/528a747ecdb5c88f843eaa9e8e59dce5/", chain_id="secret-4")
    validators = await api.staking.validators()
    validator_addresses = [v.operator_address for v in validators]

    await api.session.close()
    print(validator_addresses)


uvloop.install()
asyncio.run(main())
