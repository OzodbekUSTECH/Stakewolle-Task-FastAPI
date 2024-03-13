import requests
from pydantic import EmailStr
from app.config import settings
from app.utils.exceptions import NotVerifiedEmailException

class emailHunter:
    
    @classmethod
    def is_verified_email(cls, email:EmailStr):
        url = f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.EMAIL_HUNTER_API_KEY}'
        response = requests.get(url)
        if response.status_code == 200:
            return True
        
        else:
            raise NotVerifiedEmailException
