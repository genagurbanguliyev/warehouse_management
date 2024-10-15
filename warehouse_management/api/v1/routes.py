from fastapi import APIRouter

from warehouse_management.api.v1.endpoints.auth import router as auth_router
from warehouse_management.api.v1.endpoints.user import router as user_router
from warehouse_management.api.v1.endpoints.permission import router as permission_router
from warehouse_management.api.v1.endpoints.role import router as role_router
from warehouse_management.api.v1.endpoints.product import router as product_router
from warehouse_management.api.v1.endpoints.order import router as order_router
from warehouse_management.api.v1.endpoints.server_logs import router as server_logs_router

routers = APIRouter()
router_list = [
    auth_router,
    user_router,
    permission_router,
    role_router,
    product_router,
    order_router,
    server_logs_router,
]

for router in router_list:
    routers.include_router(router)
