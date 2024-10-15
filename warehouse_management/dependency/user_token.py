from typing import List

from dependency_injector.wiring import inject
from fastapi import Depends
from jose.jwt import decode
from jose.exceptions import JWTError, ExpiredSignatureError
from pydantic import ValidationError

from warehouse_management.core.config import configs
from warehouse_management.core.exceptions import AuthError
from warehouse_management.dependency.token import JWTBearer
from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.auth_schema import PayloadSchema
from warehouse_management.schema.user_schema import UserPublic, UserPublicWithRolePermissions
from warehouse_management.services.user_service import UserService


@inject
def get_current_user_payload(
        token: str = Depends(JWTBearer()),
) -> PayloadSchema | None:
    try:
        payload = decode(token, configs.SECRET_KEY, algorithms=configs.ALGORITHM)
        return PayloadSchema(**payload)
    except ExpiredSignatureError:
        raise AuthError(detail="Your token has expired. Please log in again.")
    except (JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")


def get_user_payload(token: str) -> PayloadSchema | None:
    try:
        payload = decode(token, configs.SECRET_KEY, algorithms=configs.ALGORITHM)
        return PayloadSchema(**payload)
    except ExpiredSignatureError:
        return None
    except (JWTError, ValidationError):
        return None


async def get_user_by_token(token: str) -> dict | None:
    current_user: PayloadSchema | None = get_user_payload(token)
    if current_user is None:
        return None
    try:
        from warehouse_management.main import container

        user_service: UserService = container.user_service()
        user: UserPublic = await user_service.get_by_id(current_user.id)
        return {"id": user.id, "username": user.username, "role": user.role}
    except Exception:
        return None


async def get_current_user_permissions(
        current_user: PayloadSchema = Depends(get_current_user_payload),
) -> List[PermissionEnum]:
    try:
        from warehouse_management.main import container, db

        auth_service: UserService = container.auth_service()
        user: UserPublicWithRolePermissions = await auth_service.get_by_id(current_user.id, get_eager=True)
        response = [permission.permission for permission in user.role_detail.permissions]
        return response
    except (JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    except Exception as err:
        raise err
