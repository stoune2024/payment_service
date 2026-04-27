from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings.settings import settings
from sqlalchemy import select
from app.schemas import Payment, Outbox

engine = create_async_engine(settings.db_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


SessionDep = Annotated[Any, Depends(get_session)]


class Repository:
    """
    Класс для взаимодействия с БД
    """

    @staticmethod
    async def get_by_idempotency_key(session, key):
        res = await session.execute(
            select(Payment).where(Payment.idempotency_key == key)
        )
        return res.scalar_one_or_none()

    @staticmethod
    async def get_payment(session, payment_id):
        res = await session.execute(select(Payment).where(Payment.id == payment_id))
        return res.scalar_one_or_none()

    @staticmethod
    async def get_unpublished(session):
        res = await session.execute(select(Outbox).where(Outbox.is_published == False))
        return res.scalars().all()
