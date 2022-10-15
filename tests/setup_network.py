import time
import subprocess
from secret_sdk.client.lcd import LCDClient


def run_command(command):
    p = subprocess.run(command.split(' '), capture_output=True)
    if p.stdout:
        print(p.stdout.decode('utf-8'))
    if p.stderr:
        print(p.stderr.decode('utf-8'))


def await_blocks():
    while True:
        try:
            secret = LCDClient(url='http://localhost:1317', chain_id='secretdev-1')
            block_info = secret.tendermint.block_info()
            latest_block = int(block_info["block"]["header"]["height"])
            if latest_block:
                print(f'Chain initialised, latest block: {latest_block}')
                break
        except Exception as e:
            print(e)
        time.sleep(5)


def setup_localsecret():
    print('Setting up LocalSecret...')

    teardown_network()
    # 9091 grpc web, 1317 rest
    run_command('docker run -it -d -p 9091:9091 -p 1317:1317 --name localsecret ghcr.io/scrtlabs/localsecret:v1.4.0')

    print("Waiting for the network to start...")
    await_blocks()

    # set block time to 200ms
    run_command('docker exec localsecret sed -E -i /timeout_(propose|prevote|precommit|commit)/s/[0-9]+m?s/200ms/ .secretd/config/config.toml')
    run_command('docker stop localsecret')
    run_command('docker start localsecret')

    await_blocks()
    print('LocalSecret is running')


def teardown_network():
    print('Tearing down local testnet...')
    run_command('docker rm -f localsecret')


if __name__ == '__main__':
    setup_localsecret()
