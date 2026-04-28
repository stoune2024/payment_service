from app.schemas import Payment, Outbox
from app.repository import Repository


async def create_payment(data, key, session):
    existing = await Repository.get_by_idempotency_key(session, key)
    if existing:
        return existing

    payment = Payment(
        amount=data.amount,
        currency=data.currency,
        description=data.description,
        extra=data.extra,
        idempotency_key=key,
        webhook_url=data.webhook_url,
    )

    session.add(payment)
    await session.flush()

    event = Outbox(event_type="payment.new", payload={"payment_id": payment.id})

    session.add(event)

    await session.commit()
    return payment
