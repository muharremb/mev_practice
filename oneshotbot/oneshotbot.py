import time
import datetime
import sys
from brownie import *

network.connect('avax-main')
user = accounts.load('eagle')

print('Loading contracts for USDT.e USDC.e Wavax Router : ')
usdt_contract = Contract.from_explorer('0xc7198437980c041c805A1EDcbA50c1Ce5db95118')
usdc_contract = Contract.from_explorer('0xA7D7079b0FEaD91F3e65f86E8915Cb59c1a4C664')
wavax_contract = Contract.from_explorer('0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7')
router_contract = Contract.from_explorer('0x60aE616a2155Ee3d9A68541Ba4544862310933d4')

usdt = {
    "address": usdt_contract.address,
    "symbol": usdt_contract.symbol(),
    "decimals": usdt_contract.decimals(),
    "balance": usdt_contract.balanceOf(user.address),
}

usdc = {
    "address": usdc_contract.address,
    "symbol": usdc_contract.symbol(),
    "decimals": usdc_contract.decimals(),
    "balance": usdc_contract.balanceOf(user.address),
}

print(f"usdc: {usdc}")
print(f"usdt: {usdt}")

if usdc["balance"] == 0:
    sys.exit('USDC balance is zero, aborting')

if usdc_contract.allowance(user.address, router_contract.address) < usdc["balance"]:
    usdc_contract.approve(router_contract.address, usdc["balance"], {'from': user.address})

last_ratio = 0.0

while True:
    try: 
        qty_out = router_contract.getAmountsOut(
            usdc["balance"],
            [
                usdc["address"],
                wavax_contract.address,
                usdt["address"]
            ]
        )[-1]
    except:
        print('Some error occured, retrying...')
        continue
    ratio = round(qty_out/usdc['balance'], 3)
    # print(f"{datetime.datetime.now().strftime('[%I:%M:%S %p]')} Regular USDC -> USDT: ({ratio:.3f})")
    if ratio != last_ratio:
        print(f"{datetime.datetime.now().strftime('[%I:%M:%S %p]')} USDC -> USDT: ({ratio:.3f})")
        last_ratio = ratio
    if ratio >= 1.01:
        print("execution")
        try: 
            router_contract.swapExactTokensForTokens(
                usdc["balance"],
                int(0.995 * qty_out),
                [
                    usdc["address"],
                    wavax_contract.address,
                    usdt["address"]
                ],
                user.address,
                1000 * int(time.time() + 30),
                {'from': user}
            )
            print('Swap Success')
        except:
            print('Swap Failed')
        finally:
            break
    time.sleep(0.5)