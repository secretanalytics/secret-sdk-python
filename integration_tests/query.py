from terra_sdk.client.lcd import LCDClient


def main():
    terra = LCDClient(
        chain_id="secret-4",
        url="https://secret-4--lcd--full.datahub.figment.io/apikey/528a747ecdb5c88f843eaa9e8e59dce5/",
    )

    result = terra.bank.balance(address="secret19y0n2ru9dae9w6vt7fwgfptp5nxq3hwtsz4u75")
    print(result)


main()
