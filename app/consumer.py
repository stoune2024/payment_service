import asyncio
import random
from datetime import datetime
from app.broker import broker
from app.repository import SessionLocal, Repository
from app.webhook import send_webhook

DLQ = "payment.dlq"


@broker.subscriber("payment.new")
async def handle(msg: dict):
    async with SessionLocal() as session:
        payment = await Repository.get_payment(session, msg["payment_id"])
        if not payment:
            return

        await asyncio.sleep(random.randint(2, 5))

        success = random.random() < 0.9
        payment.status = "succeeded" if success else "failed"
        payment.processed_at = datetime.utcnow()

        await session.commit()

        ok = await send_webhook(
            payment.webhook_url, {"payment_id": payment.id, "status": payment.status}
        )

        if not ok:
            await broker.publish(msg, routing_key=DLQ)
