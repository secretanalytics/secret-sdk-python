import asyncio

import uvloop

from secret_sdk.client.lcd import AsyncLCDClient
from integration_tests.config import api_url

async def with_sem(aw, sem):
    async with sem:
        print(sem)
        return await aw


async def main():
    api = AsyncLCDClient(url = api_url, chain_id="secret-4")
    validators = await api.staking.validators()
    validator_addresses = [v.operator_address for v in validators]

    await api.session.close()
    print(validator_addresses)


uvloop.install()
asyncio.run(main())
