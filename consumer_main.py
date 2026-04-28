import asyncio
from app.broker import broker
import app.consumer

async def main():
    while True:
        try:
            await broker.start()
            await asyncio.Event().wait()  # держим процесс живым
        except Exception:
            await asyncio.sleep(3)


asyncio.run(main())
