import asyncio
import json
import websockets
import brownie

async def pending_transactions():
    user = brownie.accounts.load('eagle')
    signed_message = user.sign_defunct_message(
        "Sign this message to authenticate your wallet with Snowsight."
    )
    async for websocket in websockets.connect(uri="ws://mempool-stream.snowsight.chainsight.dev:8589"):
        try:
            await websocket.send(
                json.dumps(
                    {"signed_key": signed_message.signature.hex()}
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
                    tx_hash = json.loads(message)
                    print('\n')
                    print(tx_hash)
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

    brownie.network.connect("public-avax-main-ws")

    await asyncio.gather(
        asyncio.create_task(pending_transactions()),
    )

if __name__ == "__main__":
    asyncio.run(main())