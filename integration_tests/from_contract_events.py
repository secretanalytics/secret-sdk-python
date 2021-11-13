from terra_sdk.client.lcd import LCDClient
from terra_sdk.util.contract import get_contract_events

tequila = LCDClient(url="https://bootstrap.secrettestnet.io", chain_id="holodeck-2")
tx_info = tequila.tx.tx_info(
    "B652DF530D50E470070F3F211519495078082D01B49ED36B762B4E9446CE484E"
)
print(get_contract_events(tx_info))
