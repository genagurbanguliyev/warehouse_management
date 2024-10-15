from warehouse_management.repository.permission_repository import PermissionRepository
from warehouse_management.services.base_service import BaseService


class PermissionService(BaseService):
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
        super().__init__(permission_repository)
