import asyncio
import json
import websockets
import brownie

async def pending_transactions():
    async for websocket in websockets.connect(uri='wss://api.avax.network/ext/bc/C/ws'):
        try:
            await websocket.send(
                json.dumps(
                    {
                        "id": 1,
                        "method": "eth_subscribe",
                        "params": ["newPendingTransactions"],
                    }
                )
            )
            subscribe_result = await websocket.recv()
            print(subscribe_result)

            while True:
                try:
                    message = await asyncio.wait_for(
                        websocket.recv(), 
                        timeout=30,
                    )
                    tx_hash = json.loads(message)["params"]["result"]
                    tx_data = brownie.web3.eth.get_transaction(tx_hash)
                    print(tx_data)
                    print('\n')
                except websockets.WebSocketException:
                    break  # escape the loop to reconnect
                except Exception as e:
                    print(e)

        except websockets.WebSocketException:
            print("reconnecting...")
            continue
        except Exception as e:
            print(e)


async def main():
    brownie.network.connect("avax-main")
    await asyncio.gather(
        asyncio.create_task(pending_transactions()),
    )

if __name__ == "__main__":
    asyncio.run(main())