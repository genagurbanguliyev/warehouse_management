from typing import List

from pydantic import BaseModel

from app.enum.permission_enum import PermissionEnum
from app.schema.base_schema import FindBaseSchema
from app.schema.permission_schema import PermissionPublic
from app.util.schema import optional


class RoleBaseSchema(BaseModel):
    role: str | None
    name: str | None


class RoleCreate(RoleBaseSchema):
    permissions: List[PermissionEnum] = []


class RolePublic(RoleBaseSchema):
    id: int


class RolePublicWithPermissions(RolePublic):
    permissions: List[PermissionPublic] | None = None

    class Config:
        from_attributes = True


class AddRemovePermission(BaseModel):
    role: str
    permissions: List[PermissionEnum]


@optional()
class FindRoleSchema(FindBaseSchema):
    role__eq: str
    ...
