from typing import List

from dependency_injector.wiring import inject
from fastapi import Depends

from app.dependency.user_token import get_current_user_permissions
from app.core.exceptions import AuthError
from app.enum.permission_enum import PermissionEnum


@inject
class PermissionChecker:
    def __init__(self, allowed_permissions: List[PermissionEnum]):
        self.allowed_permissions = allowed_permissions

    def __call__(
        self,
        user_permissions: List[PermissionEnum] = Depends(get_current_user_permissions),
    ):
        for permission in self.allowed_permissions:
            if permission not in user_permissions:
                # logger.debug(f"User with role {user['role']} not in {self.allowed_roles}")
                raise AuthError(detail="Permission denied")
