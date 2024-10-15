from typing import List

from pydantic import BaseModel, Field, ConfigDict

from warehouse_management.schema.base_schema import FindBaseSchema, FindResultSchema
from warehouse_management.util.schema import optional


class ProductBase(BaseModel):
    title: str
    quantity_in_stock: int
    desc: str


class ProductPublic(ProductBase):
    model_config = ConfigDict(extra='forbid')

    desc: str = Field(None, exclude=True)
    id: int


class ProductAllDetailsPublic(ProductPublic):
    desc: str


@optional()
class FindProductSchema(FindBaseSchema, ProductBase):
    id__in: List[int]
    quantity_in_stock__gt: int
    quantity_in_stock__lt: int


class ProductResponseSchema(FindResultSchema):
    data: List[ProductPublic]
