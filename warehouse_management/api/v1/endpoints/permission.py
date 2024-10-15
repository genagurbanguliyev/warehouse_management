from typing import List

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Form
from starlette import status

from warehouse_management.dependency.check_permission import PermissionChecker
from warehouse_management.core.container import Container
from warehouse_management.dependency.token import JWTBearer
from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.base_schema import MessageResponseBase
from warehouse_management.schema.permission_schema import PermissionPublic
from warehouse_management.services.permission_service import PermissionService

router = APIRouter(
    prefix="/permissions", tags=["Permissions"], dependencies=[Depends(JWTBearer())]
)


@router.get(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_permission]))],
    status_code=status.HTTP_200_OK,
    response_model=List[PermissionPublic],
    summary="Get all permissions",
    description="Get listed all permissions",
)
@inject
async def get_all(
    service: PermissionService = Depends(Provide[Container.permission_service]),
):
    return await service.get_all_by_options()


@router.put(
    "/{id}",
    dependencies=[Depends(PermissionChecker([PermissionEnum.manage_permission]))],
    status_code=status.HTTP_200_OK,
    response_model=MessageResponseBase,
    response_model_exclude_none=True,
    summary="Change permission name",
    description="Change permission name by id",
)
@inject
async def put(
    id: int,
    name: str = Form(...),
    service: PermissionService = Depends(Provide[Container.permission_service]),
) -> MessageResponseBase:
    await service.patch_attr(id, "name", name)
    return MessageResponseBase(message="Successfully updated")
