from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, Numeric, JSON, Boolean, Integer
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class Payment(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), nullable=False)
    description = Column(String)
    extra = Column(JSON)
    status = Column(String, default="pending")
    idempotency_key = Column(String, unique=True, nullable=False)
    webhook_url = Column(String)
    created_at = Column(DateTime, default=func.now())
    processed_at = Column(DateTime)


class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    is_published = Column(Boolean, default=False)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
