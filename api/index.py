from flask import Flask, jsonify
from web3 import Web3
from web3.middleware import geth_poa_middleware

app = Flask(__name__)

BSC_RPC = 'https://bsc-dataseed4.binance.org/'

# Treasury
CGV_ADDRESS = '0x1bDaF9ddD7658d8049391971d1fd48c0484F66EC'
TREASURY_ADDRESS = '0xc51039AD71B57E8e5B197Ee8da6340D4B8cD9612'
ERC20_ABI = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Launchpads
SDAO_ADDRESS = '0x04b269391Da04209d50aB4f4AD07a580f55E1840'
SDAO_ABI = '[{"inputs":[],"name":"reservedLaunchTokens","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

ENJIN_ADDRESS_1 = '0xe8b75734Be6F138293849D6357350Ddb8c6Bfd14'
ENJIN_ADDRESS_2 = '0x11A286b8cE9Ab6CdF93c4121E4C311CF2D91ffb1'
ENJIN_ABI = '[{"inputs":[],"name":"totalReleasedAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

w3 = Web3(Web3.HTTPProvider(BSC_RPC))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

cgv_contract = w3.eth.contract(address=CGV_ADDRESS, abi=ERC20_ABI)
sdao_contract = w3.eth.contract(address=SDAO_ADDRESS, abi=SDAO_ABI)
enjin_1_contract = w3.eth.contract(address=ENJIN_ADDRESS_1, abi=ENJIN_ABI)
enjin_2_contract = w3.eth.contract(address=ENJIN_ADDRESS_2, abi=ENJIN_ABI)


@app.route('/circulating_supply')
def circulating_supply():
    cardano_total = 100_000_000
    bsc_total = 900_000_000
    bsc_treasury = cgv_contract.functions.balanceOf(
        TREASURY_ADDRESS).call() / 1e6
    bsc_distributed = bsc_total - bsc_treasury

    sdao_locked = sdao_contract.functions.reservedLaunchTokens().call() / 1e6

    enjin_locked = 6_000_000
    enjin_1_claimed = enjin_1_contract.functions.totalReleasedAmount().call() / 1e6
    enjin_2_claimed = enjin_2_contract.functions.totalReleasedAmount().call() / 1e6

    seedify_locked = 10_000_000

    bsc_circulating = bsc_distributed - sdao_locked - enjin_locked + \
        enjin_1_claimed + enjin_2_claimed - seedify_locked

    total = bsc_circulating

    return jsonify(total)


@app.route('/total_supply')
def total_supply():
    return jsonify(1_000_000_000)
