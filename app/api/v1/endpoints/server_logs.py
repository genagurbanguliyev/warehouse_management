from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from starlette import status

from app.dependency.check_permission import PermissionChecker
from app.core.container import Container
from app.dependency.server_logs_depends import parse_server_logs_query
from app.dependency.token import JWTBearer
from app.enum.permission_enum import PermissionEnum
from app.schema.base_schema import FindResultSchema
from app.schema.server_logs_schema import FindServerLogsSchema
from app.services.server_logs_service import ServerLogsService

router = APIRouter(
    prefix="/server-logs", tags=["Logs"], dependencies=[Depends(JWTBearer())]
)


@router.get(
    "",
    dependencies=[Depends(PermissionChecker([PermissionEnum.show_server_log]))],
    status_code=status.HTTP_200_OK,
    response_model=FindResultSchema,
    summary="Get logs",
    description="Get all Server Logs",
)
@inject
async def get_all(
        find_query: FindServerLogsSchema = Depends(parse_server_logs_query),
        service: ServerLogsService = Depends(Provide[Container.server_logs_service]),
) -> FindResultSchema:
    return await service.get_all_by_options(schema=find_query, with_count=True)
