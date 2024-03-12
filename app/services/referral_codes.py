from app.schemas import referral_codes as ref_code_schema
from app.database.uow import UnitOfWork
from app import models
from app.utils.exceptions import (
    UserDoesNotHaveReferralCodeException,
    UserDoesNotExistException,
    NotAllowedToDeleteReferralCodeException
)   

from app.utils.refCode_handler import ReferralCodeHandler
from app.utils.email_handler import EmailHandler

class ReferralCodesService:

    async def create_referral_code(
            self,
            uow: UnitOfWork,
            user: models.User
    ) -> models.ReferralCode:
        async with uow:
            if user.referral_codes:
                """
                Даю сверху еще одну условие, есть ли вообще рефералки у юзера, 
                чтобы не делать лишний вопрос, который требует тоже времени больше, чем просто условие
                """
                has_one_active_ref_code: models.ReferralCode = await uow.referral_codes.get_one_active_ref_code_or_none_of_user(user_id=user.id)
                
                if has_one_active_ref_code:
                    
                    """
                    Если есть одно активное, то перед созданием нового,
                    мы деактивируем уже существующий
                    """
                    has_one_active_ref_code.is_active = False
            

            #Теперь создаем уникальный реферал!
            while True:
                generated_ref_code = ReferralCodeHandler.generate_referral_code(length=16)
                existing_ref_code = await uow.referral_codes.get_one_or_none(code=generated_ref_code)
                if not existing_ref_code:
                    break  # если не найден существующий реферальный код, выходим из цикла

            expiration_date = ReferralCodeHandler.generate_expiration_date()

            referral_code_data = ref_code_schema.CreateReferralCodeSchema(
                user_id=user.id,
                code=generated_ref_code,
                expiration_date=expiration_date
            ).model_dump()

            created_referral_code = await uow.referral_codes.create(data=referral_code_data)
            await uow.commit()
            return created_referral_code
        
    async def get_referral_codes_of_user(
            self,
            uow: UnitOfWork,
            user_id: int
    ) -> models.ReferralCode:
        async with uow:
            user: models.User = await uow.users.get_by_id(id=user_id)
            return await uow.referral_codes.get_all(user_id=user.id)
        
    async def send_referral_code_to_email(
            self,
            uow: UnitOfWork,
            email: str
    ):
        async with uow:
            user_with_given_email: models.User = await uow.users.get_one_or_none(email=email)
            if not user_with_given_email:
                raise UserDoesNotExistException
            active_referral_code_of_user = await uow.referral_codes.get_one_active_ref_code_or_none_of_user(user_id=user_with_given_email.id)
            if not active_referral_code_of_user:
                active_referral_code_of_user = await self.create_referral_code(uow=uow, user=user_with_given_email)

            body = f"ВАШ РЕФЕРАЛЬНЫЙ КОД: {active_referral_code_of_user.code}\nИстекает: {active_referral_code_of_user.expiration_date.strftime("%d/%m/%Y, %H:%M:%S")}"
               
            return await EmailHandler.send_message(
                emails=email,
                subject="REFERRAL CODE",
                body=body,
            )

            
                
    async def delete_referral_code(
            self,
            uow: UnitOfWork,
            id: int
    ) -> ref_code_schema.ReferralCodeSchema:
        async with uow:
            referral_code = await uow.referral_codes.delete(id=id)
            await uow.commit()
            return referral_code

ref_codes_service = ReferralCodesService()