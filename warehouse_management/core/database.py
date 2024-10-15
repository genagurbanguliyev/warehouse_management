from contextlib import asynccontextmanager, AbstractAsyncContextManager
from typing import Callable, Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_url: str) -> None:
        self._sync_engine = create_engine(url=db_url, echo=False)
        self._async_engine = create_async_engine(url=db_url, future=True, echo=False)
        self._async_session_factory = async_scoped_session(
            session_factory=async_sessionmaker(
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
                future=True,
                bind=self._async_engine,
            ),
            scopefunc=self.get_scope,
        )

    @staticmethod
    def get_scope() -> Any:
        import asyncio
        return asyncio.current_task()

    @asynccontextmanager
    async def async_session(
            self,
    ) -> Callable[..., AbstractAsyncContextManager[AsyncSession]]:
        async_session: AsyncSession = self._async_session_factory()
        try:
            yield async_session
        except Exception as error:
            print("ERROR in the Session============== ", error)
            logger.error(error)
            await async_session.rollback()
            raise
        finally:
            await async_session.close()
