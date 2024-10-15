from fastapi import Depends

from warehouse_management.enum.log_status_enum import LogStatusEnum
from warehouse_management.schema.server_logs_schema import QueryServerLogsSchema, FindServerLogsSchema
from warehouse_management.util.date import parse_datetime


async def parse_server_logs_query(query_data: QueryServerLogsSchema = Depends()):
    schema = FindServerLogsSchema()
    schema.message__in = (
        query_data.query
        if query_data.query and query_data.query != ""
        else None
    )
    schema.action__in = (
        query_data.query
        if query_data.query and query_data.query != ""
        else None
    )
    schema.status__eq = LogStatusEnum(query_data.status.lower()) if query_data.status else None
    schema.module = query_data.module if query_data.module else None
    schema.method = query_data.method if query_data.method else None
    schema.created_at__gt = (
        parse_datetime(query_data.start_date)
        if query_data.start_date and query_data.start_date != ""
        else None
    )
    schema.created_at__lt = (
        parse_datetime(query_data.end_date)
        if query_data.end_date and query_data.end_date != ""
        else None
    )
    schema.page = query_data.page
    schema.limit = query_data.limit

    for key, value in schema.model_dump().items():
        if value is None:
            delattr(schema, key)

    return schema
