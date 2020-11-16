from binance_chain.environment import BinanceEnvironment
from binance_chain.http import HttpApiClient
from binance_chain.wallet import Wallet

testnet_env = BinanceEnvironment.get_testnet_env()
client = HttpApiClient(env=testnet_env)


def make_binance_wallet():
    wallet = Wallet.create_random_wallet(env=testnet_env)
    print(wallet.address)
    print(wallet.private_key)
    print(wallet.public_key_hex)
    return wallet.address
