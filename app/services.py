from app.schemas import Payment, Outbox
from app.repository import Repository


async def create_payment(data, key, session):
    existing = await Repository.get_by_idempotency_key(session, key)
    if existing:
        return existing

    payment = Payment(**data.model_dump(), idempotency_key=key)

    event = Outbox(event_type="payment.new", payload={"payment_id": payment.id})

    session.add(payment)
    session.add(event)

    await session.commit()
    return payment
