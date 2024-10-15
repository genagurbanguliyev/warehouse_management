from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from warehouse_management.dependency.check_permission import PermissionChecker
from warehouse_management.core.container import Container
from warehouse_management.dependency.token import JWTBearer
from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.base_schema import MessageResponseBase
from warehouse_management.schema.role_schema import (
    RolePublicWithPermissions,
    RoleCreate,
    AddRemovePermission, RoleBaseSchema
)
from warehouse_management.services.permission_service import PermissionService
from warehouse_management.services.role_service import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(JWTBearer())]
)


@router.post(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_role]))],
    status_code=status.HTTP_200_OK,
    response_model=RolePublicWithPermissions,
    response_model_exclude_none=True,
    summary="Create role",
    description="Create a new role",
)
@inject
async def create(
    info: RoleCreate,
    service: RoleService = Depends(Provide[Container.role_service]),
) -> RolePublicWithPermissions:
    return await service.create(info)


@router.get(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_role]))],
    status_code=status.HTTP_200_OK,
    response_model=list[RolePublicWithPermissions],
    summary="Get all roles",
    description="Get Listed all roles",
)
@inject
async def get_all(
    service: RoleService = Depends(Provide[Container.role_service]),
) -> list[RolePublicWithPermissions]:
    return await service.get_all_by_options()


@router.get(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_role]))],
    status_code=status.HTTP_200_OK,
    response_model=RolePublicWithPermissions,
    summary="Get role details",
    description="Get role details by id",
)
@inject
async def get_one(
    id: int,
    service: RoleService = Depends(Provide[Container.role_service]),
) -> RolePublicWithPermissions:
    return await service.get_by_id(id, True)


@router.put(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_role]))],
    status_code=status.HTTP_200_OK,
    response_model=RolePublicWithPermissions,
    response_model_exclude_none=True,
    summary="Edit role & name",
    description="Edit role & name",
)
@inject
async def put(
    id: int,
    info: RoleBaseSchema,
    service: RoleService = Depends(Provide[Container.role_service]),
) -> RolePublicWithPermissions:
    return await service.edit_role(id, info)


@router.patch(
    "/add-permission",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_role]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Add permission",
    description="Add new permissions to a role",
)
@inject
async def add_permission(
    info: AddRemovePermission,
    service: RoleService = Depends(Provide[Container.role_service]),
    permission_service: PermissionService = Depends(
        Provide[Container.permission_service]
    ),
) -> MessageResponseBase:
    return await service.add_permission(info, permission_service)


@router.patch(
    "/remove-permission",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_role]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Remove permission",
    description="Remove role's permissions",
)
@inject
async def add_permission(
    info: AddRemovePermission,
    service: RoleService = Depends(Provide[Container.role_service]),
) -> MessageResponseBase:
    return await service.remove_permission(info)


@router.delete(
    "/{role}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_role]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Delete role",
    description="Delete role",
)
@inject
async def delete(
    role: str,
    service: RoleService = Depends(Provide[Container.role_service]),
) -> MessageResponseBase:
    return await service.remove_by_attr(role)
