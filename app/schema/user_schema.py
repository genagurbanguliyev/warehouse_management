from pydantic import BaseModel, Field, ConfigDict

from app.schema.auth_schema import LoginSchema
from app.schema.base_schema import (
    FindBaseSchema,
)
from app.schema.role_schema import RolePublicWithPermissions
from app.util.schema import optional


class ChangePassword(BaseModel):
    password: str
    new_password: str


class UserPublic(BaseModel):
    id: int
    username: str
    name: str
    role: str


class RegistrationSchema(LoginSchema):
    name: str


class CreateUserSchema(LoginSchema):
    name: str
    role: str


@optional()
class FindUserSchema(UserPublic):
    ...


class UserModelSchema(UserPublic):
    password: str


class UserPublicWithRolePermissions(UserPublic):
    model_config = ConfigDict(from_attributes=True)

    role_detail: RolePublicWithPermissions | None = None
