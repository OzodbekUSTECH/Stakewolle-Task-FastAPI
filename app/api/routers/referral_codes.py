from fastapi import APIRouter, Depends
from app.services.referral_codes import ref_codes_service
from app.database.uow import UOW_DEP
from app.schemas import referral_codes as ref_code_schema
from app.dependencies import CURRENT_USER_DEP
from app.permissions import Permissions
from fastapi_pagination import Page
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix="/referrals",
    tags=["Referral Codes"]
)


@router.post('/')
async def create_referral_code(
    uow: UOW_DEP,
    current_user: CURRENT_USER_DEP
) -> ref_code_schema.ReferralCodeSchema:
    return await ref_codes_service.create_referral_code(
        uow=uow,
        user=current_user
    )

@router.post('/to/email')
async def send_referral_code_to_email(
    uow: UOW_DEP,
    email: str
):
    """
    Возможность получения реферального кода по email адресу реферера.\n
    Я понял это так:\n
    - Если реферальный код есть у пользователя, то сервис должен отправить его реферальный код на электронную почту реферера.
    - НО НЕ ВОЗВРАЩАЕТ ИНФОРМАЦИЮ РЕФ. КОДА НА ЗАПРОС! ВМЕСТО ЭТОГО ПРОСТО СООБЩЕНИЕ

    - ЭТОТ ENDPOINT наверное лучше сделать, как background_task, но для удостоверения, что всё отправлено успешно,
    то можно оставить так
    """
    return await ref_codes_service.send_referral_code_to_email(
        uow=uow,
        email=email
    )


"""
@cache - кешируем данные, 
    - expire=300 в секундах (5 мин кеш)
"""
@router.get('/{user_id}')
@cache(namespace="ref_codes", expire=300)
async def get_referral_codes_of_user_by_id(
    uow: UOW_DEP,
    user_id: int
) -> Page[ref_code_schema.ReferralCodeSchema]:
    """
    получение информации о рефералах по id реферера
    """
    return await ref_codes_service.get_referral_codes_of_user(
        uow=uow,
        user_id=user_id
    )


@router.delete('/{id}', dependencies=[Depends(Permissions.is_referral_belongs_to_current_user)])
async def delete_referral_code(
    uow: UOW_DEP,
    id: int
) -> ref_code_schema.ReferralCodeSchema:
    return await ref_codes_service.delete_referral_code(
        uow=uow,
        id=id
    )