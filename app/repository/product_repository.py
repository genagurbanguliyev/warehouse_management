from contextlib import AbstractAsyncContextManager
from typing import Callable, List

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import InternalError
from app.model import ProductModel
from app.repository.base_repository import BaseRepository
from app.schema.base_schema import MessageResponseBase


class ProductRepository(BaseRepository):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.async_session_factory = async_session_factory
        super().__init__(async_session_factory, ProductModel)
