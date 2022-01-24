from secret_sdk.core.staking import Validator


def test_deserializes():
    # /staking/validators/secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7
    validator_data = {
        "operator_address": "secretvaloper18762353s6ulgla3efvf0hpe5rjjxp5ndfvl8z7",
        "consensus_pubkey": {
          "type": "tendermint/PubKeyEd25519",
          "value": "LCh8vJCJcTpi1X+uaOWWN/GsP73YrgySVeprqakdhyE="
        },
        "status": 3,
        "jailed": False,
        "tokens": "1481239420813",
        "delegator_shares": "1481239420813.000000000000000000",
        "description": {
          "moniker": "SCRT LabRador",
          "identity": "030EC99E4095C506",
          "website": "https://scrt.network/",
          "details": "Community run node of eng OG ICO holders and privacy advocates (2017) supporting the network since day 1, 99% uptime guaranteed - with refund - hosted in various dedicated data centers.",
          "security_contact": None
        },
        "unbonding_height": "813800",
        "unbonding_time": "0001-01-22T00:00:00Z",
        "commission": {
          "commission_rates": {
            "rate": "0.000000000000000000",
            "max_rate": "0.200000000000000000",
            "max_change_rate": "0.010000000000000000"
          },
          "update_time": "2021-01-24T23:45:49.923630005Z"
        },
        "min_self_delegation": "1"
    }

    assert validator_data == Validator.from_data(validator_data).to_data()
