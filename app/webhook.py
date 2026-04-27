import httpx
import asyncio


async def send_webhook(url, payload):
    delay = 1
    for _ in range(3):
        try:
            async with httpx.AsyncClient() as client:
                await client.post(url, json=payload)
            return True
        except Exception:
            await asyncio.sleep(delay)
            delay *= 2
    return False
