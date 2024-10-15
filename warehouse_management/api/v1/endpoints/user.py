from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from warehouse_management.dependency.check_permission import PermissionChecker
from warehouse_management.core.container import Container
from warehouse_management.dependency.user_token import get_current_user_payload
from warehouse_management.dependency.token import JWTBearer
from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.auth_schema import PayloadSchema
from warehouse_management.schema.base_schema import MessageResponseBase
from warehouse_management.schema.user_schema import ChangePassword, UserPublicWithRolePermissions, UserPublic, FindUserSchema, CreateUserSchema
from warehouse_management.services.user_service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(JWTBearer())],
)


@router.post(
    "/create-user",
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
    summary="Registration",
    description="Creates user with given details",
)
@inject
async def create_user(
    user_info: CreateUserSchema,
    service: UserService = Depends(Provide[Container.user_service]),
) -> UserPublic:
    return await service.create_user(user_info)


@router.get(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_user]))],
    status_code=status.HTTP_200_OK,
    response_model=List[UserPublic],
    summary="Get all Users",
    description="Get list all users",
)
@inject
async def get_all(
        find_query: FindUserSchema = Depends(),
        service: UserService = Depends(Provide[Container.user_service]),
) -> List[UserPublic]:
    return await service.get_all_by_options(schema=find_query)


@router.get(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_user]))],
    status_code=status.HTTP_200_OK,
    response_model=UserPublicWithRolePermissions,
    summary="Get User details",
    description="Get User details by id",
)
@inject
async def get_one(
        id: int,
        service: UserService = Depends(Provide[Container.user_service])
) -> UserPublicWithRolePermissions:
    return await service.get_by_id(id, get_eager=True)


@router.patch(
    "/password",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_user]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Change password",
    description="Change password with authenticated user",
)
@inject
async def change_password(
        user_info: ChangePassword,
        service: UserService = Depends(Provide[Container.user_service]),
        current_user: PayloadSchema = Depends(get_current_user_payload),
) -> MessageResponseBase:
    return await service.change_password(current_user.id, user_info)
