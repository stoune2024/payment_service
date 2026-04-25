from pydantic import BaseModel
from typing import Optional, Dict


class PaymentCreate(BaseModel):
    amount: float
    currency: str
    description: Optional[str] = None
    metadata: Optional[Dict] = None
    webhook_url: str
