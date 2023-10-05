from lib.date_utils import MINUTE

BNB_BNB_SYMBOL = 'BNB.BNB'

BNB_BUSD_SYMBOL = 'BNB.BUSD-BD1'
BNB_BUSD_TEST_SYMBOL = 'BNB.BUSD-BAF'
BNB_BUSD_TEST2_SYMBOL = 'BNB.BUSD-74E'

BNB_BTCB_SYMBOL = 'BNB.BTCB-1DE'
BNB_BTCB_TEST_SYMBOL = 'BNB.BTCB-101'
BTC_SYMBOL = 'BTC.BTC'
BCH_SYMBOL = 'BCH.BCH'

NATIVE_RUNE_SYMBOL = 'THOR.RUNE'
RUNE_SYMBOL = NATIVE_RUNE_SYMBOL

RUNE_SYMBOL_DET = 'RUNE-DET'
RUNE_SYMBOL_POOL = 'RUNE-MARKET'
RUNE_SYMBOL_CEX = 'RUNE-MARKET-CEX'

BNB_ETHB_SYMBOL = 'BNB.ETH-1C9'
BNB_ETHB_TEST_SYMBOL = 'BNB.ETH-D5B'
ETH_SYMBOL = 'ETH.ETH'
AVAX_SYMBOL = 'AVAX.AVAX'

BNB_USDT_SYMBOL = 'BNB.USDT-6D8'
BNB_USDT_TEST_SYMBOL = 'BNB.USDT-DC8'
ETH_USDT_TEST_SYMBOL = 'ETH.USDT-0XA3910454BF2CB59B8B3A401589A3BACC5CA42306'
ETH_USDT_SYMBOL = 'ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'
ETH_USDC_SYMBOL = 'ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'
ETH_DAI_SYMBOL = 'ETH.DAI-0X6B175474E89094C44DA98B954EEDEAC495271D0F'
AVAX_USDC_SYMBOL = 'AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E'
BSC_BUSD_SYMBOL = 'BSC.BUSD-0XE9E7CEA3DEDCA5984780BAFC599BD69ADD087D56'

DOGE_SYMBOL = 'DOGE.DOGE'

RUNE_IDEAL_SUPPLY = 500_000_000
RUNE_SUPPLY_AFTER_SWITCH = 486_051_059


def is_rune(symbol):
    return symbol == NATIVE_RUNE_SYMBOL


class Chains:
    THOR = 'THOR'
    ETH = 'ETH'
    BTC = 'BTC'
    BCH = 'BCH'
    LTC = 'LTC'
    BNB = 'BNB'
    DOGE = 'DOGE'
    TERRA = 'TERRA'  # bye-bye
    AVAX = 'AVAX'
    ATOM = 'GAIA'
    BSC = 'BSC'

    META_ALL = (THOR, ETH, BTC, BCH, LTC, BNB, DOGE, AVAX, ATOM, BSC)

    @staticmethod
    def detect_chain(orig_address: str) -> str:
        address = orig_address.lower()
        if address.startswith('0x'):
            return Chains.ETH  # or other EVM chain??
        elif address.startswith('terra'):
            return Chains.TERRA
        elif address.startswith('thor') or address.startswith('tthor') or address.startswith('sthor'):
            return Chains.THOR
        elif address.startswith('bnb') or address.startswith('tbnb'):
            return Chains.BNB
        elif orig_address.startswith('D'):
            return Chains.DOGE
        elif address.startswith('cosmos'):
            return Chains.ATOM
        return ''

    @staticmethod
    def block_time_default(chain: str) -> float:
        if chain == Chains.ETH:
            return 13
        elif chain == Chains.BTC or chain == Chains.BCH:
            return 10 * MINUTE
        elif chain == Chains.LTC:
            return 2.5 * MINUTE
        elif chain == Chains.BNB:
            return 0.4
        elif chain == Chains.THOR:
            return THOR_BLOCK_TIME
        elif chain == Chains.DOGE:
            return MINUTE
        elif chain == Chains.TERRA:
            return 6.64
        elif chain == Chains.ATOM:
            return 6.85
        elif chain == Chains.AVAX:
            return 3.0
        elif chain == Chains.BSC:
            return 3.0
        return 0.01

    @staticmethod
    def web3_chain_id(chain: str) -> int:
        if chain == Chains.ETH:
            return 0x1
        elif chain == Chains.AVAX:
            return 43114
        elif chain == Chains.BSC:
            return 56

    @staticmethod
    def l1_asset(chain: str) -> str:
        assert chain in Chains.META_ALL
        return f'{chain}.{chain}'


class NetworkIdents:
    TESTNET_MULTICHAIN = 'testnet-multi'
    CHAOSNET_MULTICHAIN = 'chaosnet-multi'
    MAINNET = 'mainnet'
    STAGENET_MULTICHAIN = 'stagenet-multi'

    @classmethod
    def is_test(cls, network: str):
        return 'testnet' in network

    @classmethod
    def is_live(cls, network: str):
        return not cls.is_test(network)

    @classmethod
    def is_multi(cls, network: str):
        return 'multi' in network or network == cls.MAINNET


RUNE_DECIMALS = 8
THOR_DIVIDER = float(10 ** RUNE_DECIMALS)
THOR_DIVIDER_INV = 1.0 / THOR_DIVIDER

THOR_BLOCK_TIME = 6.0  # seconds. 10 blocks / minute
THOR_BLOCK_SPEED = 1 / THOR_BLOCK_TIME
THOR_BLOCKS_PER_MINUTE = MINUTE * THOR_BLOCK_SPEED

THOR_BASIS_POINT_MAX = 10_000


def bp_to_float(bp):
    return int(bp) / THOR_BASIS_POINT_MAX


def bp_to_percent(bp):
    return bp_to_float(bp) * 100.0


def thor_to_float(x) -> float:
    return int(x) * THOR_DIVIDER_INV


def float_to_thor(x: float) -> int:
    return int(x * THOR_DIVIDER)


BLOCKS_PER_YEAR = 5_256_000

DEFAULT_RUNE_FEE = 2000000

DEFAULT_RESERVE_ADDRESS = 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'
BOND_MODULE = 'thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv'
POOL_MODULE = 'thor1g98cy3n9mmjrpn0sxmn63lztelera37n8n67c0'
SYNTH_MODULE = 'thor1v8ppstuf6e3x0r4glqc68d5jqcs2tf38cg2q6y'
