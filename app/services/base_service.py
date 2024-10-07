from typing import TypeVar, Any, List, Generic
from pydantic import BaseModel

TSchema = TypeVar("TSchema", bound=BaseModel)


class BaseService(Generic[TSchema]):
    def __init__(self, repository) -> None:
        self._repository = repository

    async def get_all_by_options(
        self, schema: TSchema | None = None, get_eager: bool = False, with_count: bool = False
    ):
        return await self._repository.read_all_by_options(schema, get_eager, with_count)

    async def get_one_by_options(
        self, schema: TSchema | None = None, get_eager: bool = False, not_found_error: bool = False
    ):
        return await self._repository.read_one_by_options(schema, get_eager, not_found_error)

    async def get_by_id(self, query_id: int, get_eager: bool = False, not_found_error: bool = True):
        return await self._repository.read_by_id(
            query_id=query_id, get_eager=get_eager, not_found_error=not_found_error
        )

    async def add(self, schema: TSchema):
        return await self._repository.create(schema)

    async def patch_attr(self, query_id: int, attr: str, value: Any):
        return await self._repository.update_attr(query_id, attr, value)

    async def put_update(self, query_id: int, schema: TSchema):
        return await self._repository.update(query_id, schema)

    async def remove_by_id(self, query_id: int):
        return await self._repository.delete_by_id(query_id)

    async def remove_multiple_by_ids(self, ids: List[int]):
        return await self._repository.delete_multiple_by_ids(ids)
