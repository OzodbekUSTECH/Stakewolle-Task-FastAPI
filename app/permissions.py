from app.dependencies import CURRENT_USER_DEP
from app.database.uow import UOW_DEP
from app.utils.exceptions import  ReferralCodeExpiredException, ReferralCodeDoesNotExistException, NotAllowedMethodException
from fastapi import Request
from app import models
from datetime import datetime

class Permissions:

    @classmethod
    async def is_referral_belongs_to_current_user(cls, request: Request, uow: UOW_DEP, current_user: CURRENT_USER_DEP) -> bool:
        referral_code_id = int(request.path_params.get("id"))
        async with uow:
            referral_code: models.ReferralCode = await uow.referral_codes.get_one_or_none(id=referral_code_id)
            if not referral_code:
                raise ReferralCodeDoesNotExistException
            elif referral_code.user_id != current_user.id:
                raise NotAllowedMethodException
            return True
                
        
    
    @classmethod
    async def is_referral_code_given_and_unexpired(cls, request: Request, uow: UOW_DEP) -> bool:
        referral_code = request.query_params.get("referral_code")
        if referral_code: #ПЕРЕДАЛИ ЛИ РЕФ.КОД 
            async with uow:
                existing_ref_code: models.ReferralCode = await uow.referral_codes.get_one_or_none(code=referral_code)
                if not existing_ref_code:
                    raise ReferralCodeDoesNotExistException
                elif existing_ref_code.expiration_date.timestamp() > datetime.utcnow().timestamp():
                    existing_ref_code.is_active = False
                    await uow.commit()
                    raise ReferralCodeExpiredException
            
        return True