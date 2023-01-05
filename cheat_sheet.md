# MEV Learning

## Brownie
It is a framework that wraps web3.py library

### Create a User
> brownie accounts generate test_account

### Connect to network
> brownie networks modify avax-main

modify just prints current settings

## How to fork avax to local ganache
Brownie provides ganache-cli development environment.
> brownie console --network avax-main-fork

## Local Mainnet Fork
First set environment variable 
> export WEB3_INFURA_PROJECT_ID=YourProjectID
Run following command to connect local fork
> brownie console --network mainnet-fork

## Vyper
Use event
> event eventName:
>   value: uint256

In the function
> log eventName(variableName)

In the console, after calling function, add .info()
> contract.funct().info()

## Uniswap Router Contract interaction 
getAmountsOut(amountIn, path)
swapExactTokensForTokens(amountIn, amountOutMin, path, address to, deadline)

To swap using a Router, first grant approval for that input token to that Router address, such as 
xxx.approve(router.address, AMOUNT, {'from': ACCOUNT })