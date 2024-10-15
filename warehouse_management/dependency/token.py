from datetime import datetime, timedelta

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from starlette import status
from starlette.requests import Request

from warehouse_management.core.config import configs
from warehouse_management.core.exceptions import AuthError


def create_access_token(subject: dict, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=configs.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"exp": expire, **subject}
    return jwt.encode(payload, configs.SECRET_KEY, algorithm=configs.ALGORITHM)


def decode_jwt(token: str) -> dict | None:
    try:
        decoded_token = jwt.decode(
            token, configs.SECRET_KEY, algorithms=configs.ALGORITHM
        )
        return (
            decoded_token
            if decoded_token["exp"] >= int(round(datetime.utcnow().timestamp()))
            else None
        )
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str:
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthError(
                    status=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme.",
                )
            if not self.verify_jwt(credentials.credentials):
                raise AuthError(
                    status=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise AuthError(
                status=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization code.",
            )

    @staticmethod
    def verify_jwt(jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
