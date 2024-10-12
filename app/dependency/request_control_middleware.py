import json
from typing import Dict, Any

from dependency_injector.wiring import inject
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi.routing import APIRoute

from app.api.v1.routes import router_list
from app.core.container import Container
from app.dependency.user_token import get_user_by_token
from app.enum.log_status_enum import LogStatusEnum
from app.schema.server_logs_schema import ServerLogsUpsert


@inject
class RequestControlMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        # if request.url.path.startswith("/docs") or request.url.path.startswith("/api/openapi.json"):
        #     print("url path---------------------------------------- ", request.url.path)
        #     return await call_next(request)
        # try:
        server_log_service = Container().server_logs_service()
        route_info = self.get_route_info(request)
        query_params = dict(request.query_params)

        log_data = await self.create_audit_log(request, route_info, query_params)
        request.state.audit = log_data
        response = await call_next(request)
        if response.status_code < 400:
            await server_log_service.save_log(request.state.audit)
            return response
        else:
            request.state.audit = log_data
            return response
        # except Exception as error:
        #     print("dispatch method error====================== ", error)

    async def create_audit_log(
            self, request: Request, route_info: dict | None, query_params: dict | None
    ) -> ServerLogsUpsert:
        auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            user_data = json.dumps(await get_user_by_token(auth_header.split(" ")[1]))
        else:
            user_data = None

        request_body: str | None = await self.get_req_body(request)
        log_data = ServerLogsUpsert()
        log_data.user = user_data
        log_data.method = str(request.method)
        log_data.ip_address = str(request.client.host)
        log_data.body = request_body
        log_data.status = LogStatusEnum.success.value
        log_data.ip_address = request.client.host

        if route_info:
            log_data.module = route_info["name"]
            log_data.action = route_info["summary"]
            log_data.message = route_info["description"]
        if query_params:
            if log_data.message is not None:
                log_data.message += f" |query options: {request.query_params}"
        return log_data

    @staticmethod
    def get_route_info(request: Request) -> Dict[str, Any]:
        request_path = request.scope["path"].split("/")
        query_id: str = ""
        for router in router_list:
            for route in router.routes:
                if request_path[-1].isdigit():
                    query_id = f"id={request_path[-1]}"
                    request_path[-1] = "{id}"
                if isinstance(route, APIRoute) and route.path == "/".join(request_path):
                    for method in route.methods:
                        if method == request.method:
                            return {
                                "name": (
                                    router.tags[0] if router.tags[0] else route.name
                                ),
                                "summary": route.summary if route.summary else "",
                                "description": (
                                    f"{route.description} {query_id}"
                                    if route.description
                                    else ""
                                ),
                            }

    @staticmethod
    async def get_req_body(request: Request) -> str | None:
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body = await request.json()
                if isinstance(body, dict):  # Convert dict to a JSON string
                    return json.dumps(body)
                elif isinstance(body, list):  # Convert list to a JSON string
                    return json.dumps(body)
                elif isinstance(body, str):  # If it's already a string
                    return body
            except Exception as error:
                # Handle exceptions if the request body is not a valid JSON
                print(f"Failed to parse request body: {error}")
                return None
        return None
