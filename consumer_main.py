import asyncio
from app.broker import broker


async def main():
    while True:
        try:
            await broker.start()
            await broker.run()
        except Exception as e:
            print(f"Broker connection failed: {e}")
            await asyncio.sleep(3)


asyncio.run(main())
