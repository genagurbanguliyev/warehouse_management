from dependency_injector.wiring import Provide
from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.core.container import Container
from app.enum.log_status_enum import LogStatusEnum
from app.schema.base_schema import MessageResponseBase
from app.services.server_logs_service import ServerLogsService
from app.util.date import get_now

import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(
        request,
        exc,
        server_log_service: ServerLogsService = Depends(
            Provide[Container.server_logs_service]
        ),
):
    content = MessageResponseBase(status=exc.status_code, message=str(exc.detail), timestamp=str(get_now())).model_dump(mode="json")
    if request.state.audit:
        request.state.audit.message = content["message"]
        request.state.audit.status = LogStatusEnum.field
    await server_log_service.save_log(request.state.audit)
    logger.error(content)
    return JSONResponse(jsonable_encoder(content), status_code=exc.status_code)


async def req_validation_exception_handler(
        request,
        exc,
        server_log_service: ServerLogsService = Depends(
            Provide[Container.server_logs_service]
        ),
):
    content = MessageResponseBase(
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=f"Invalid data provided: {str(exc)}",
        timestamp=str(get_now()),
    ).model_dump(mode="json")
    if request.state.audit:
        request.state.audit.message = content["message"]
        request.state.audit.status = LogStatusEnum.field
    await server_log_service.save_log(request.state.audit)
    logger.error(content)
    return JSONResponse(jsonable_encoder(content), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


async def res_validation_exception_handler(
        request,
        exc,
        server_log_service: ServerLogsService = Depends(
            Provide[Container.server_logs_service]
        ),
):
    content = MessageResponseBase(
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=f"Invalid data provided: {str(exc)}",
        timestamp=str(get_now()),
    ).model_dump(mode="json")
    if request.state.audit:
        request.state.audit.message = content["message"]
        request.state.audit.status = LogStatusEnum.field
    await server_log_service.save_log(request.state.audit)
    logger.error(content)
    return JSONResponse(jsonable_encoder(content), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
