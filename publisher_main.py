import asyncio
from app.publisher import run_publisher
from app.broker import broker


async def main():
    while True:
        try:
            await broker.start()
            await run_publisher()
        except Exception as e:
            print(f"Publisher failed: {e}")
            await asyncio.sleep(3)


asyncio.run(main())
