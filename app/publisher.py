import asyncio
from app.repository import SessionLocal, Repository
from app.broker import broker


async def run_publisher():
    while True:
        async with SessionLocal() as session:
            events = await Repository.get_unpublished(session)

            for event in events:
                try:
                    await broker.publish(event.payload, routing_key=event.event_type)
                    event.is_published = True
                except Exception:
                    event.retry_count += 1

            await session.commit()

        await asyncio.sleep(1)
