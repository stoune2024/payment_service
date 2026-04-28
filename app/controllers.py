from typing import Annotated

from fastapi import APIRouter, Request, HTTPException, status, Header
from app.models import PaymentCreate
from app.services import create_payment
from app.repository import SessionDep, Repository
from settings.settings import settings

router = APIRouter(tags=["Работа с платежами"])


@router.post("/payments", status_code=202)
async def create_payment_handler(
    request: Request,
    data: PaymentCreate,
    session: SessionDep,
    x_api_key: Annotated[
        str | None, Header()
    ] = None,  # нужен для ручного ввода в Swagger UI
    idempotency_key: Annotated[
        str | None, Header()
    ] = None,  # нужен для ручного ввода в Swagger UI
    content_type: Annotated[
        str | None, Header()
    ] = None,  # нужен для ручного ввода в Swagger UI
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


@router.get("/payments/{payment_id}")
async def get_payment(
    request: Request,
    payment_id: str,
    session: SessionDep,
    x_api_key: Annotated[
        str | None, Header()
    ] = None,  # нужен для ручного ввода в Swagger UI
):
    if request.headers.get("X-API-Key") != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API-key отсутствует или недействителен",
        )

    payment = await Repository.get_payment(session, payment_id)

    if not payment:
        raise HTTPException(status_code=404, detail="Платеж не найден")

    return payment
