from typing import Type
from app.database.core import async_session_maker
from app import repositories
from app import models
from typing import Annotated
from fastapi import Depends




class UnitOfWork:
    users: Type[repositories.UsersRepository]
    referral_codes: Type[repositories.ReferralCodesRepository]


    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = repositories.UsersRepository(session=self.session, model=models.User)
        self.referral_codes = repositories.ReferralCodesRepository(session=self.session, model=models.ReferralCode)
        

    async def __aexit__(self, *args):    
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()



UOW_DEP = Annotated[UnitOfWork, Depends()]