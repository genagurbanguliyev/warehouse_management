from typing import List

from pydantic import BaseModel, Field

from app.schema.base_schema import FindBaseSchema, FindResultSchema
from app.util.schema import optional


class ProductBase(BaseModel):
    title: str
    quantity_in_stock: int
    desc: str


class ProductPublic(ProductBase):
    desc: str = Field(None, exclude=True)
    id: int

    class Config:
        extra = 'forbid'


class ProductAllDetailsPublic(ProductPublic):
    desc: str


@optional()
class FindProductSchema(FindBaseSchema, ProductBase):
    id__in: List[int] | int
    quantity_in_stock__gt: int
    quantity_in_stock__lt: int


class ProductResponseSchema(FindResultSchema):
    data: List[ProductPublic]
