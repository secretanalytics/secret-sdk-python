from secret_sdk.client.lcd import LCDClient
from integration_tests.config import api_url


def main():
    secret = LCDClient(
        chain_id="secret-4",
        url=api_url,
    )

    result = secret.bank.balance(address="secret19y0n2ru9dae9w6vt7fwgfptp5nxq3hwtsz4u75")
    print(result)


main()
