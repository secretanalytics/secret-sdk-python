import asynctest
from secret_sdk.client.lcd import LCDClient
from aioresponses import aioresponses


TxKey = '{"height":"991131","result":{"TxKey":"CDsaA2YSEdWkzI05p3eVeVhi93MGRVc7K8wsGSDFPAQ="}}'


class TestDoSessionGet(asynctest.TestCase):
    @aioresponses()
    def test_makes_request_to_expected_url(self, mocked):
        mocked.get('https://bootstrap.secrettestnet.io/reg/tx-key', status=200, body=TxKey)
        mocked.get('https://bootstrap.secrettestnet.io/node_info', status=200, body='{"response": "test"}')
        terra = LCDClient(chain_id="holodeck-2", url="https://bootstrap.secrettestnet.io")

        resp = terra.tendermint.node_info()

        assert resp == {"response": "test"}

    @aioresponses()
    def test_does_not_strip_access_token(self, mocked):
        mocked.get('https://bootstrap.secrettestnet.io/access_token/reg/tx-key', status=200, body=TxKey)
        mocked.get('https://bootstrap.secrettestnet.io/access_token/node_info', status=200, body='{"response": "test"}')
        terra = LCDClient(chain_id="holodeck-2", url="https://bootstrap.secrettestnet.io/access_token/")

        resp = terra.tendermint.node_info()

        assert resp == {"response": "test"}


if __name__ == '__main__':
    asynctest.main()
