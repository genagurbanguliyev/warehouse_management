from fastapi import Query

from app.core.exceptions import ValidationError, InternalError
from app.schema.product_schema import FindProductSchema


async def parse_product_query(
        query: str | None = Query(None),
        page: int | None = Query(None),
        limit: int | None = Query(None),
        quantity_more_than: str | None = Query(None),
        quantity_less_than: str | None = Query(None)
):
    try:
        schema = FindProductSchema()
        schema.title = query if query is not None and query != "" else None
        schema.page = int(page) if page is not None and page != "" and page != "null" else None
        schema.limit = int(limit) if limit is not None and limit != "" and limit != "null" else None
        schema.quantity_in_stock__gt = (
            int(quantity_more_than)
            if quantity_more_than is not None and quantity_more_than != ""
            else None
        )
        schema.quantity_in_stock__lt = (
            int(quantity_less_than)
            if quantity_less_than is not None and quantity_less_than != ""
            else None
        )

        for key, value in schema.model_dump().items():
            if value is None:
                delattr(schema, key)

        return schema
    except ValueError as error:
        raise ValidationError(detail=str(error))
    except Exception as error:
        raise InternalError(detail=str(error))
