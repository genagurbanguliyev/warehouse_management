from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from warehouse_management.core.exceptions import InternalError
from warehouse_management.model import ProductModel
from warehouse_management.repository.base_repository import BaseRepository
from warehouse_management.schema.base_schema import MessageResponseBase


class ProductRepository(BaseRepository):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.async_session_factory = async_session_factory
        super().__init__(async_session_factory, ProductModel)
