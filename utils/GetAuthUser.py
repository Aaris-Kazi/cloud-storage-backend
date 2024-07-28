from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.request import Request

def GetUser(request: Request) -> str:
    token = str(request.auth)
    decoded_token = AccessToken(token)
    return str(decoded_token['user_id'])