from fastapi import HTTPException

from app.repository.role_repository import RoleRepository
from app.schema.base_schema import MessageResponseBase
from app.schema.role_schema import (
    FindRoleSchema,
    RoleCreate,
    RolePublicWithPermissions,
    AddRemovePermission,
    RoleBaseSchema
)
from app.services.base_service import BaseService
from app.services.permission_service import PermissionService


class RoleService(BaseService):
    def __init__(self, role_repository: RoleRepository):
        self.role_repository = role_repository
        super().__init__(role_repository)

    async def create(self, data: RoleCreate) -> RolePublicWithPermissions:
        data.role = data.role.strip().lower()
        await self.role_repository.find_or_dublicated(
            data.role, dublicated_error=True
        )
        return await self.role_repository.create_role(data)

    async def edit_role(
            self,
            query_id: int,
            data: RoleBaseSchema,
    ) -> RolePublicWithPermissions:
        return await self.role_repository.update_role(query_id, data)

    async def add_permission(
            self, data: AddRemovePermission, permission_service: PermissionService
    ):
        found: RolePublicWithPermissions = (
            await self.role_repository.find_or_dublicated(data.role)
        )
        return await self.role_repository.add_new_permissions(
            data, found, permission_service
        )

    async def remove_permission(self, data: AddRemovePermission):
        found: RolePublicWithPermissions = (
            await self.role_repository.find_or_dublicated(data.role)
        )
        return await self.role_repository.remove_permissions(data, found)

    async def remove_by_attr(self, role: str) -> MessageResponseBase:
        find = FindRoleSchema()
        find.role__eq = role
        await self.role_repository.delete_by_attr(find)
        return MessageResponseBase(message="Role successfully deleted")
