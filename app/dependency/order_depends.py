from fastapi import Query

from app.core.exceptions import ValidationError, InternalError
from app.enum.order_enum import OrderStatusEnum
from app.schema.order_schema import FindOrderSchema
from app.util.date import parse_datetime


async def parse_order_query(
        status: str | None = Query(None),
        page: int | None = Query(None),
        limit: int | None = Query(None),
        start_date: str | None = Query(None),
        end_date: str | None = Query(None),
):
    try:
        schema = FindOrderSchema()
        schema.page = int(page) if page is not None and page != "" and page != "null" else None
        schema.limit = int(limit) if limit is not None and limit != "" and limit != "null" else None
        schema.status__eq = (
            OrderStatusEnum(status)
            if status is not None and status != "null" and status != ""
            else None
        )
        schema.created_at__gt = (
            parse_datetime(start_date)
            if start_date is not None and start_date != ""
            else None
        )
        schema.created_at__lt = (
            parse_datetime(end_date) if end_date is not None and end_date != "" else None
        )

        for key, value in schema.model_dump().items():
            if value is None:
                delattr(schema, key)

        return schema
    except ValueError as error:
        raise ValidationError(detail=str(error))
    except Exception as error:
        raise InternalError(detail=str(error))
