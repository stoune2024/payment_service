from fastapi import APIRouter, Request, HTTPException, status
from app.models import PaymentCreate
from app.services import create_payment
from app.repository import SessionDep
from settings.settings import settings

router = APIRouter(tags=["Работа с платежами"])


@router.post("/payments", status_code=202)
async def create_payment_handler(
    request: Request, data: PaymentCreate, session: SessionDep
):
    if request.headers.get("X-API-Key") != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API-key отсутствует или недействителен",
        )

    key = request.headers.get("Idempotency-Key")
    if not key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Отсутсвтует ключ идемпотентности",
        )

    payment = await create_payment(data, key, session)

    return {
        "payment_id": payment.id,
        "status": payment.status,
        "created_at": payment.created_at,
    }
