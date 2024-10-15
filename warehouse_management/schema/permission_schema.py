from pydantic import BaseModel, ConfigDict

from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.base_schema import FindBaseSchema
from warehouse_management.util.schema import optional


class PermissionBase(BaseModel):
    name: str
    permission: PermissionEnum


class PermissionPublic(PermissionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


@optional()
class PermissionUpsert(PermissionBase):
    ...


@optional()
class FindPermissionSchema(PermissionPublic, FindBaseSchema):
    permission__eq: str
    ...


