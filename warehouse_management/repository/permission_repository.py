from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_management.core.exceptions import DublicatedError
from warehouse_management.model.permission import PermissionModel
from warehouse_management.repository.base_repository import BaseRepository
from warehouse_management.schema.permission_schema import FindPermissionSchema, PermissionBase


class PermissionRepository(BaseRepository):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.async_session_factory = async_session_factory
        super().__init__(async_session_factory, PermissionModel)

    async def find_or_dublicated(
            self, info: PermissionBase, dublicated_error: bool = False
    ) -> PermissionModel:
        find = FindPermissionSchema()
        find.permission__eq = info.permission
        found_response: PermissionModel = await self.read_one_by_options(schema=find)
        if found_response and dublicated_error:
            raise DublicatedError(detail="permission already existed")
        return found_response
