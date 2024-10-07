from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.exceptions import DublicatedError
from app.model import PermissionModel, RolePermissionsModel
from app.schema.permission_schema import PermissionUpsert
from app.model.role import RoleModel
from app.repository.base_repository import BaseRepository
from app.schema.base_schema import MessageResponseBase
from app.schema.role_schema import (
    FindRoleSchema,
    RolePublicWithPermissions,
    RolePublic,
    RoleBaseSchema,
    AddRemovePermission
)
from app.services.permission_service import PermissionService


class RoleRepository(BaseRepository):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.async_session_factory = async_session_factory
        super().__init__(async_session_factory, RoleModel)

    async def find_or_dublicated(
            self, role: str, dublicated_error: bool = False
    ) -> RolePublic | RolePublicWithPermissions:
        find = FindRoleSchema()
        find.role__eq = role
        found_response = await self.read_one_by_options(schema=find)
        if found_response and dublicated_error:
            raise DublicatedError(detail="Role already existed")
        return found_response

    async def create_role(self, schema: RoleBaseSchema):
        permissions_data = schema.model_dump().pop("permissions", [])

        async with self.async_session_factory() as async_session:
            query = self.model(
                **{k: v for k, v in schema.model_dump().items() if k != "permissions"}
            )

            for permission in permissions_data:
                linked = await async_session.execute(
                    select(PermissionModel).where(
                        PermissionModel.permission == permission
                    )
                )
                res: PermissionModel = linked.scalar_one_or_none()
                query.permissions.append(res)
            async_session.add(query)
            await async_session.commit()
            await async_session.refresh(query)
            return query

    async def update_role(
            self,
            query_id: int,
            schema: RoleBaseSchema,
    ) -> RolePublicWithPermissions:
        async with self.async_session_factory() as async_session:
            q = update(self.model).where(self.model.id == query_id).values(**schema.model_dump())
            await async_session.execute(q)
            await async_session.commit()
            return await self.read_by_id(query_id)

    async def remove_permissions(
            self,
            schema: AddRemovePermission,
            old_data: RolePublicWithPermissions,
    ) -> MessageResponseBase:
        permissions_data = schema.model_dump().pop("permissions", [])
        async with self.async_session_factory() as async_session:
            if len(permissions_data):
                for permission in permissions_data:
                    await async_session.execute(
                        delete(RolePermissionsModel)
                        .where(RolePermissionsModel.role == old_data.role)
                        .where(RolePermissionsModel.permission == permission)
                    )
                    await async_session.commit()

            return MessageResponseBase(message="Permission removed")

    async def add_new_permissions(
            self,
            schema: AddRemovePermission,
            old_data: RolePublicWithPermissions,
            permission_service: PermissionService,
    ) -> MessageResponseBase:
        permissions_data = schema.model_dump().pop("permissions", [])
        async with self.async_session_factory() as async_session:
            query = self.model(
                **{k: v for k, v in schema.model_dump().items() if k != "permissions"}
            )
            query.role = old_data.role

            if len(permissions_data):
                for permission in permissions_data:
                    role_permission = await async_session.execute(
                        select(RolePermissionsModel)
                        .where(RolePermissionsModel.role == query.role)
                        .where(RolePermissionsModel.permission == permission)
                    )
                    role_permission = role_permission.scalar_one_or_none()
                    if not role_permission:
                        linked: PermissionModel = (
                            await permission_service.permission_repository.find_or_dublicated(
                                PermissionUpsert(permission=permission)
                            )
                        )
                        query.permissions.append(linked)
                        role_permission_link = RolePermissionsModel(
                            role=query.role, permission=permission
                        )
                        async_session.add(role_permission_link)
                        await async_session.commit()
            return MessageResponseBase(message="Permission added")
