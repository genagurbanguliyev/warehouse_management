from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.core.container import Container
from app.schema.auth_schema import LoginSchema, PayloadSchema
from app.schema.user_schema import RegistrationSchema

from app.dependency.user_token import get_current_user_payload
from app.schema.user_schema import UserPublicWithRolePermissions
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth", tags=["Auth"]
)


@router.post(
    "/login",
    status_code=status.HTTP_201_CREATED,
    summary="Login",
    description="Get token as a string",
)
@inject
async def login(
    user_info: LoginSchema,
    service: AuthService = Depends(Provide[Container.auth_service]),
) -> str:
    return await service.login(user_info)


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=PayloadSchema,
    summary="Registration",
    description="Sign up user with given details",
)
@inject
async def registration(
    user_info: RegistrationSchema,
    service: AuthService = Depends(Provide[Container.auth_service]),
) -> PayloadSchema:
    return await service.registration(user_info)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserPublicWithRolePermissions,
    summary="User information from token",
    description="Get full information about authenticated user",
)
@inject
async def get_me(
    service: AuthService = Depends(Provide[Container.auth_service]),
    current_user: PayloadSchema = Depends(get_current_user_payload),
) -> UserPublicWithRolePermissions:
    return await service.get_by_id(current_user.id, get_eager=True)
