from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from warehouse_management.dependency.check_permission import PermissionChecker
from warehouse_management.core.container import Container
from warehouse_management.dependency.server_logs_depends import parse_server_logs_query
from warehouse_management.dependency.token import JWTBearer
from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.schema.server_logs_schema import FindServerLogsSchema, ServerLogsResponse
from warehouse_management.services.server_logs_service import ServerLogsService

router = APIRouter(
    prefix="/server-logs", tags=["Logs"], dependencies=[Depends(JWTBearer())]
)


@router.get(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_server_log]))],
    status_code=status.HTTP_200_OK,
    response_model=ServerLogsResponse,
    summary="Get logs",
    description="Get all Server Logs",
)
@inject
async def get_all(
        find_query: FindServerLogsSchema = Depends(parse_server_logs_query),
        service: ServerLogsService = Depends(Provide[Container.server_logs_service]),
) -> ServerLogsResponse:
    return await service.get_all_by_options(schema=find_query, with_count=True)
