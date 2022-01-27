import asynctest
from aioresponses import aioresponses

from secret_sdk.client.lcd import LCDClient

TxKey = '{"height":"991131","result":{"TxKey":"CDsaA2YSEdWkzI05p3eVeVhi93MGRVc7K8wsGSDFPAQ="}}'


class TestDoSessionGet(asynctest.TestCase):
    @aioresponses()
    def test_makes_request_to_expected_url(self, mocked):
        mocked.get(
            "http://testnet.securesecrets.org:1317/reg/tx-key", status=200, body=TxKey
        )
        mocked.get(
            "http://testnet.securesecrets.org:1317/node_info",
            status=200,
            body='{"response": "test"}',
        )
        secret = LCDClient(
            chain_id="pulsar-2", url="http://testnet.securesecrets.org:1317"
        )

        resp = secret.tendermint.node_info()

        assert resp == {"response": "test"}

    @aioresponses()
    def test_does_not_strip_access_token(self, mocked):
        mocked.get(
            "http://testnet.securesecrets.org:1317/access_token/reg/tx-key",
            status=200,
            body=TxKey,
        )
        mocked.get(
            "http://testnet.securesecrets.org:1317/access_token/node_info",
            status=200,
            body='{"response": "test"}',
        )
        secret = LCDClient(
            chain_id="pulsar-2",
            url="http://testnet.securesecrets.org:1317/access_token/",
        )

        resp = secret.tendermint.node_info()

        assert resp == {"response": "test"}


if __name__ == "__main__":
    asynctest.main()
