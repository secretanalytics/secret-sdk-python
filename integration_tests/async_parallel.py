import asyncio
import uvloop

from secret_sdk.client.localsecret import AsyncLocalSecret


async def with_sem(aw, sem):
    async with sem:
        print(sem)
        return await aw


async def main():
    async with AsyncLocalSecret(chain_id="pulsar-2") as secret:
        validators = await secret.staking.validators()
        validator_addresses = [v.operator_address for v in validators]

        await secret.session.close()
        print(validator_addresses)


uvloop.install()
asyncio.run(main())
