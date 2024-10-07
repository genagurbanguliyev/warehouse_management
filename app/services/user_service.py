from fastapi import HTTPException

from app.core.exceptions import AuthError
from app.core.password import verify_password, get_password_hash
from app.repository.user_repository import UserRepository
from app.schema.base_schema import MessageResponseBase
from app.schema.user_schema import ChangePassword, UserPublic, CreateUserSchema
from app.services.base_service import BaseService


class UserService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def create_user(self, data: CreateUserSchema):
        data.password = get_password_hash(data.password)
        return await self.add(data)

    async def change_password(
            self, user_id: int, data: ChangePassword
    ) -> MessageResponseBase:
        try:
            found_user: UserPublic = await self.get_by_id(user_id)
            if not verify_password(data.password, found_user.password):
                raise AuthError(detail="Incorrect password")

            await self.patch_attr(
                user_id, "password", get_password_hash(data.new_password)
            )
            return MessageResponseBase(message="Password changed")
        except HTTPException as err:
            raise err
