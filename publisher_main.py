import asyncio
from app.publisher import run_publisher
from app.broker import broker


async def main():
    await broker.start()
    await run_publisher()


asyncio.run(main())
