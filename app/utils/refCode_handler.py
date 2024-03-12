
import random
import string
from datetime import datetime, timedelta

class ReferralCodeHandler:

    @classmethod
    def generate_referral_code(cls, length: int = 8):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @classmethod
    def generate_expiration_date(cls):
        return datetime.now() + timedelta(days=30)