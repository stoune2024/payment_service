import asyncio
from app.broker import broker


async def main():
    await broker.start()
    await broker.run()


asyncio.run(main())
