from contextlib import AbstractAsyncContextManager
from typing import Callable, Generic, List

from fastapi import HTTPException
from sqlalchemy import func, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.future import select

from warehouse_management.core.config import configs
from warehouse_management.core.exceptions import NotFoundError, DublicatedError, InternalError
from warehouse_management.model.base_model import Base
from warehouse_management.schema.base_schema import FindResultSchema, MessageResponseBase
from warehouse_management.services.base_service import TSchema
from warehouse_management.util.query_builder import dict_to_sqlalchemy_filter_options


class BaseRepository(Generic[TSchema]):
    def __init__(
            self,
            async_session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
            model: type[Base],
    ) -> None:
        self.async_session_factory = async_session_factory
        self.model = model

    async def read_all_by_options(
            self, schema: TSchema | None, get_eager: bool = False, with_count: bool = False
    ):
        async with self.async_session_factory() as async_session:
            try:
                query = select(self.model)
                if schema is not None:
                    schema_as_dict = schema.model_dump(exclude_none=True)
                    ordering = schema_as_dict.get("ordering", configs.ORDERING)
                    order_query = (
                        getattr(self.model, ordering[1:]).desc()
                        if ordering.startswith("-")
                        else getattr(self.model, ordering).asc()
                    )
                    page = schema_as_dict.get("page", configs.PAGE)
                    page_size = schema_as_dict.get("limit", configs.PAGE_SIZE) if with_count else "all"
                    filter_options = dict_to_sqlalchemy_filter_options(
                        self.model, schema.model_dump(exclude_none=True)
                    )
                    query = query.filter(filter_options).order_by(order_query)
                    if page_size != "all":
                        query = query.limit(int(page_size)).offset(
                            (page - 1) * int(page_size)
                        )

                if get_eager:
                    for eager in getattr(self.model, "eagers", []):
                        query = query.options(selectinload(getattr(self.model, eager)))

                results = await async_session.execute(query)
                founds = results.scalars().all()
                if with_count:
                    total_count_query = select(func.count()).select_from(
                        select(self.model).filter(filter_options).subquery()
                    )
                    total_count = await async_session.scalar(total_count_query)
                    return FindResultSchema(data=founds, total=total_count)
                else:
                    return founds
            except Exception as error:
                raise InternalError(detail=str(error))

    async def read_one_by_options(
            self,
            schema: TSchema,
            get_eager: bool = False,
            not_found_error: bool = False,
    ):
        async with self.async_session_factory() as async_session:
            try:
                filter_options = dict_to_sqlalchemy_filter_options(
                    self.model, schema.model_dump(exclude_none=True)
                )
                query = select(self.model).filter(filter_options).limit(1)
                if get_eager:
                    for eager in getattr(self.model, "eagers", []):
                        query = query.options(joinedload(getattr(self.model, eager)))

                result = await async_session.execute(query)
                instance = result.scalar_one_or_none()
                if not instance and not_found_error:
                    raise NotFoundError(detail="Not found with given options")
                return instance
            except NotFoundError:
                raise NotFoundError(detail="Not found with given options")
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def read_by_id(
            self, query_id: int, get_eager: bool = False, not_found_error: bool = False
    ):
        async with self.async_session_factory() as async_session:
            try:
                query = select(self.model).filter(self.model.id == query_id)
                if get_eager:
                    for eager in getattr(self.model, "eagers", []):
                        query = query.options(selectinload(getattr(self.model, eager)))
                result = await async_session.execute(query)
                instance = result.scalar_one_or_none()
                if instance is None and not_found_error:
                    raise NotFoundError(detail=f"Not found id: {query_id}")
                return instance
            except NotFoundError:
                raise NotFoundError(detail="Not found with given options")
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def create(self, schema: TSchema):
        async with self.async_session_factory() as async_session:
            try:
                query = self.model(**schema.model_dump())
                async_session.add(query)
                await async_session.commit()
                await async_session.refresh(query)
                return query
            except IntegrityError as error:
                raise DublicatedError(detail=str(error.orig))
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def update(self, query_id: int, schema: TSchema):
        async with self.async_session_factory() as async_session:
            try:
                await async_session.execute(
                    update(self.model)
                    .where(self.model.id == query_id)
                    .values(schema.model_dump(exclude_none=True))
                )
                await async_session.commit()
                return await self.read_by_id(query_id, not_found_error=True)
            except NotFoundError:
                raise NotFoundError(detail="Not found with given options")
            except IntegrityError as error:
                raise DublicatedError(detail=str(error.orig))
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def update_attr(self, query_id: int, column: str, value):
        async with self.async_session_factory() as async_session:
            try:
                await async_session.execute(
                    update(self.model)
                    .where(self.model.id == query_id)
                    .values({column: value})
                )
                await async_session.commit()
                return await self.read_by_id(query_id, not_found_error=True)
            except NotFoundError:
                raise NotFoundError(detail="Not found with given options")
            except IntegrityError as error:
                raise DublicatedError(detail=str(error.orig))
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def delete_by_id(self, query_id: int):
        async with self.async_session_factory() as async_session:
            try:
                instance = await self.read_by_id(query_id, not_found_error=True)
                await async_session.delete(instance)
                await async_session.commit()
            except NotFoundError as error:
                raise NotFoundError(detail=error)
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def delete_by_attr(self, schema: TSchema):
        async with self.async_session_factory() as async_session:
            try:
                result = await self.read_one_by_options(schema)
                await async_session.delete(result)
                await async_session.commit()
            except NotFoundError:
                raise NotFoundError(detail="Not found with given options")
            except HTTPException as error:
                raise InternalError(detail=str(error))

    async def delete_multiple_by_ids(self, ids: List[int]):
        async with self.async_session_factory() as async_session:
            try:
                query_update = (
                    delete(self.model)
                    .where(self.model.id.in_(ids))
                )
                await async_session.execute(query_update)
                await async_session.commit()
            except NotFoundError:
                raise NotFoundError(detail="Not found with given options")
            except HTTPException as error:
                raise InternalError(detail=str(error))
