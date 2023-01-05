# @version >=0.3.2

interface IUniswapV2Factory:
    def getPair(
        tokenA: address, 
        tokenB: address,
    ) -> address: view

interface IUniswapV2Pair:
    def token0() -> address: view
    def token1() -> address: view
    def getReserves() -> (uint112, uint112, uint32): view

@external
@view
def get_pair_from_factory(
    factory_address: address, 
    tokenA: address, 
    tokenB: address,
) -> address:
    assert tokenA != tokenB, "token addresses must be different!"
    return IUniswapV2Factory(factory_address).getPair(tokenA, tokenB)

@external
@view
def get_reserves_from_liquidity_pool(pool_address: address) -> (uint112, uint112):
    reserve0: uint112 = 0
    reserve1: uint112 = 0
    time_stamp: uint32 = 0
     
    reserve0, reserve1, time_stamp = IUniswapV2Pair(pool_address).getReserves()
    return reserve0, reserve1

@external
@view
def get_tokens_in_pool(pool_address:address) -> (address, address):
    return IUniswapV2Pair(pool_address).token0(), IUniswapV2Pair(pool_address).token1()