from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.user import router as user_router
from app.api.v1.endpoints.permission import router as permission_router
from app.api.v1.endpoints.role import router as role_router
from app.api.v1.endpoints.product import router as product_router
from app.api.v1.endpoints.order import router as order_router
from app.api.v1.endpoints.server_logs import router as server_logs_router

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
    # router.tags = routers.tags.append("v1")
    routers.include_router(router)
