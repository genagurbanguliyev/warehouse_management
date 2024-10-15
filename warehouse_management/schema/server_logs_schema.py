from datetime import datetime
from typing import List

from pydantic import Field, BaseModel

from warehouse_management.enum.log_status_enum import LogStatusEnum
from warehouse_management.schema.base_schema import FindBaseSchema, FindResultSchema
from warehouse_management.util.schema import optional


class ServerLogsBase(BaseModel):
    module: str | None
    method: str | None
    message: str | None
    status: LogStatusEnum | None
    action: str | None
    ip_address: str | None
    user: str | None
    body: str | None


@optional()
class ServerLogsUpsert(ServerLogsBase):
    ...


@optional()
class QueryServerLogsSchema(FindBaseSchema):
    module: str | None = Field(None)
    status: str | None = Field(None)
    method: str | None = Field(None)
    start_date: str | None = Field(None)
    end_date: str | None = Field(None)
    ...


@optional()
class FindServerLogsSchema(FindBaseSchema, ServerLogsBase):
    id__in: List[int] | int
    status__eq: LogStatusEnum | None
    message__in: str | None
    action__in: str | None
    created_at__gt: datetime | str
    created_at__lt: datetime | str


class ServerLogsResponse(FindResultSchema):
    data: List[ServerLogsBase]
