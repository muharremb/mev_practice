import time
import datetime
from brownie import *

network.connect('avax-main')
user = accounts.load('test_account')

print('Loding Contracts: ')
dai_contract = Contract.from_explorer('0xd586E7F844cEa2F87f50152665BCbc2C279D8d70')
usdc_contract = Contract.from_explorer('0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664')
usdt_contract = Contract.from_explorer('0xc7198437980c041c805A1EDcbA50c1Ce5db95118')
wavax_contract = Contract.from_explorer('0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7')
router_contract = Contract.from_explorer('0x60aE616a2155Ee3d9A68541Ba4544862310933d4')

dai = {
    "address": dai_contract.address,
    "symbol": dai_contract.symbol(),
    "decimals": dai_contract.decimals(),
}
usdc = {
    "address": usdc_contract.address,
    "symbol": usdc_contract.symbol(),
    "decimals": usdc_contract.decimals(),
}
usdt = {
    "address": usdt_contract.address,
    "symbol": usdt_contract.symbol(),
    "decimals": usdt_contract.decimals(),
}

token_pairs = [
    (dai, usdc),
    (dai, usdt),
    (usdc, dai),
    (usdc, usdt),
    (usdt, dai),
    (usdt, usdc),
]

while True:
    for pair in token_pairs:
        token_in = pair[0]
        token_out = pair[1]
        qty_out = (
            router_contract.getAmountsOut(
                1 * (10 ** token_in['decimals']),
                [
                    token_in['address'],
                    wavax_contract.address,
                    token_out['address']
                ],
            )[-1] / (10 ** token_out['decimals'])
        )
        print(
            f"{datetime.datetime.now().strftime('[%I:%M:%S %p]')} {token_in['symbol']} -> {token_out['symbol']}: ({qty_out:.3f})"
        )
        time.sleep(1.0)