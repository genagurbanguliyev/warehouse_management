from warehouse_management.core.exceptions import AuthError
from warehouse_management.core.password import verify_password, get_password_hash
from warehouse_management.dependency.token import create_access_token
from warehouse_management.repository.user_repository import UserRepository
from warehouse_management.schema.auth_schema import LoginSchema, PayloadSchema
from warehouse_management.schema.user_schema import FindUserSchema, RegistrationSchema, CreateUserSchema
from warehouse_management.services.base_service import BaseService


class AuthService(BaseService):
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        super().__init__(user_repository)

    async def login(self, login_info: LoginSchema) -> str:
        try:
            finder = FindUserSchema()
            finder.username = login_info.username
            found_user = (await self.user_repository.read_one_by_options(
                schema=finder,
                not_found_error=True
            ))
            if not verify_password(login_info.password, found_user.password):
                raise AuthError(detail="Incorrect password")
            payload = PayloadSchema(id=found_user.id, username=found_user.username)
            return create_access_token(payload.model_dump())
        except Exception as error:
            raise error

    async def registration(self, user_info: RegistrationSchema) -> PayloadSchema:
        user = CreateUserSchema(**user_info.model_dump(), role="client")
        user.password = get_password_hash(user_info.password)
        return await self.add(user)
