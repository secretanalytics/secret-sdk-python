from secret_sdk.core.staking import Delegation, Redelegation, UnbondingDelegation


# /staking/delegators/secret1axk8d8hmpradn7k33x95r8dvq77tajg8v6hn5e/unbonding_delegations
def test_deserialize_unbonding_delegation_examples(load_json_examples):
    examples = load_json_examples("./UnbondingDelegation.data.json")
    for example in examples:
        assert UnbondingDelegation.from_data(example).to_data() == example

# /staking/delegators/secret1axk8d8hmpradn7k33x95r8dvq77tajg8v6hn5e/delegations
def test_deserialize_delegation_examples(load_json_examples):
    examples = load_json_examples("./Delegation.data.json")
    for example in examples:
        assert Delegation.from_data(example).to_data() == example

# /staking/redelegations
def test_deserialize_redelegation_examples(load_json_examples):
    examples = load_json_examples("./Redelegation.data.json")
    for example in examples:
        assert Redelegation.from_data(example).to_data() == example
