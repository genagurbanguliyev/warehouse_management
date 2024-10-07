from pydantic import BaseModel

from app.enum.permission_enum import PermissionEnum
from app.schema.base_schema import FindBaseSchema
from app.util.schema import optional


class PermissionBase(BaseModel):
    name: str
    permission: PermissionEnum


class PermissionPublic(PermissionBase):
    id: int

    class Config:
        from_attributes = True


@optional()
class PermissionUpsert(PermissionBase):
    ...


@optional()
class FindPermissionSchema(PermissionPublic, FindBaseSchema):
    permission__eq: str
    ...


