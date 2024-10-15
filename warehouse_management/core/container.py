from dependency_injector import containers, providers

from warehouse_management.core.config import configs
from warehouse_management.core.database import Database

from warehouse_management.repository.order_repository import OrderRepository
from warehouse_management.repository.permission_repository import PermissionRepository
from warehouse_management.repository.product_repository import ProductRepository
from warehouse_management.repository.role_repository import RoleRepository
from warehouse_management.repository.server_logs_repository import ServerLogsRepository
from warehouse_management.repository.user_repository import UserRepository

from warehouse_management.services.auth_service import AuthService
from warehouse_management.services.user_service import UserService
from warehouse_management.services.permission_service import PermissionService
from warehouse_management.services.product_service import ProductService
from warehouse_management.services.role_service import RoleService
from warehouse_management.services.order_service import OrderService
from warehouse_management.services.server_logs_service import ServerLogsService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "warehouse_management.api.v1.endpoints.auth",
            "warehouse_management.api.v1.endpoints.user",
            "warehouse_management.api.v1.endpoints.permission",
            "warehouse_management.api.v1.endpoints.role",
            "warehouse_management.api.v1.endpoints.product",
            "warehouse_management.api.v1.endpoints.order",
            "warehouse_management.api.v1.endpoints.server_logs",
        ]
    )

    db = providers.Singleton(Database, db_url=configs.DATABASE_URL)

    user_repository = providers.Factory(
        UserRepository, async_session_factory=db.provided.async_session
    )
    role_repository = providers.Factory(
        RoleRepository, async_session_factory=db.provided.async_session
    )
    permission_repository = providers.Factory(
        PermissionRepository, async_session_factory=db.provided.async_session
    )
    product_repository = providers.Factory(
        ProductRepository, async_session_factory=db.provided.async_session
    )
    order_repository = providers.Factory(
        OrderRepository, async_session_factory=db.provided.async_session,product_repository=product_repository
    )
    server_logs_repository = providers.Factory(
        ServerLogsRepository, async_session_factory=db.provided.async_session
    )

    auth_service = providers.Factory(AuthService, user_repository=user_repository)
    user_service = providers.Factory(UserService, user_repository=user_repository)
    role_service = providers.Factory(RoleService, role_repository=role_repository)
    permission_service = providers.Factory(PermissionService, permission_repository=permission_repository)
    product_service = providers.Factory(ProductService, product_repository=product_repository)
    order_service = providers.Factory(OrderService, order_repository=order_repository)

    server_logs_service = providers.Factory(ServerLogsService, server_logs_repository=server_logs_repository)
