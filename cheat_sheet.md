# MEV Learning

## Brownie
It is a framework that wraps web3.py library

### Create a User
> brownie accounts generate test_account

### Connect to network
> brownie networks modify avax-main

modify just prints current settings

## Uniswap Router Contract interaction 
getAmountsOut(amountIn, path)
swapExactTokensForTokens(amountIn, amountOutMin, path, address to, deadline)

To swap using a Router, first grant approval for that input token to that Router address, such as 
xxx.approve(router.address, AMOUNT, {'from': ACCOUNT })