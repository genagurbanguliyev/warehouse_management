from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_management.model.server_logs import ServerLogsModel
from warehouse_management.repository.base_repository import BaseRepository


class ServerLogsRepository(BaseRepository):
    def __init__(
        self,
        async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.async_session_factory = async_session_factory
        super().__init__(async_session_factory, ServerLogsModel)
