from secret_sdk.client.lcd import LCDClient
from integration_tests.config import api_url

secret = LCDClient(
    chain_id="secret-4",
    url = api_url,
)

res = secret.auth.account_info(address="secret19y0n2ru9dae9w6vt7fwgfptp5nxq3hwtsz4u75")
print(res)

res = secret.auth.account_info(address="secret1c7rjffp9clkvrzul20yy60yhy6arnv7sde0kjj")
print(res)
