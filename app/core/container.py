from dependency_injector import containers, providers

from app.core.config import configs
from app.core.database import Database

from app.repository.order_repository import OrderRepository
from app.repository.permission_repository import PermissionRepository
from app.repository.product_repository import ProductRepository
from app.repository.role_repository import RoleRepository
from app.repository.server_logs_repository import ServerLogsRepository
from app.repository.user_repository import UserRepository

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.permission_service import PermissionService
from app.services.product_service import ProductService
from app.services.role_service import RoleService
from app.services.order_service import OrderService
from app.services.server_logs_service import ServerLogsService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "app.api.v1.endpoints.auth",
            "app.api.v1.endpoints.user",
            "app.api.v1.endpoints.permission",
            "app.api.v1.endpoints.role",
            "app.api.v1.endpoints.product",
            "app.api.v1.endpoints.order",
            "app.api.v1.endpoints.server_logs",
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
        OrderRepository, async_session_factory=db.provided.async_session
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
