from app.api.routers.auth import router as router_auth
from app.api.routers.referral_codes import router as router_referral_codes

all_routers = [
    router_auth,
    router_referral_codes
]