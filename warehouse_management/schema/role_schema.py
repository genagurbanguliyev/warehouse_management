from typing import List

from pydantic import BaseModel, ConfigDict

from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.base_schema import FindBaseSchema
from warehouse_management.schema.permission_schema import PermissionPublic
from warehouse_management.util.schema import optional


class RoleBaseSchema(BaseModel):
    role: str | None
    name: str | None


class RoleCreate(RoleBaseSchema):
    permissions: List[PermissionEnum] = []


class RolePublic(RoleBaseSchema):
    id: int


class RolePublicWithPermissions(RolePublic):
    model_config = ConfigDict(from_attributes=True)

    permissions: List[PermissionPublic] | None = None


class AddRemovePermission(BaseModel):
    role: str
    permissions: List[PermissionEnum]


@optional()
class FindRoleSchema(FindBaseSchema):
    role__eq: str
    ...
