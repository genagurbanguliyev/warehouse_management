from datetime import datetime
from typing import List

from pydantic import BaseModel, Field, ConfigDict

from warehouse_management.enum.order_enum import OrderStatusEnum
from warehouse_management.schema.base_schema import FindBaseSchema, FindResultSchema
from warehouse_management.schema.order_item_schema import OrderItemSchema
from warehouse_management.schema.product_schema import ProductPublic
from warehouse_management.schema.user_schema import UserPublic
from warehouse_management.util.schema import optional


class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    delivery_address: str


class OrderCreate(OrderBase):
    products: List[OrderItemSchema]


class OrderCreateSchema(OrderCreate):
    username: str
    status: OrderStatusEnum = Field(default=OrderStatusEnum.in_process)
    ...


class OrderPublic(OrderBase):
    id: int
    created_at: datetime
    status: OrderStatusEnum


class OrderPublicWithProducts(OrderPublic):
    products: List[ProductPublic]


class OrderPublicWithProductsAndUser(OrderPublicWithProducts):
    user_detail: UserPublic | None


@optional()
class FindOrderSchema(FindBaseSchema):
    id: int | None
    username: str | None
    id__in: List[int]
    status__eq: OrderStatusEnum
    created_at__gt: datetime | str
    created_at__lt: datetime | str


class OrderResponseSchema(FindResultSchema):
    data: List[OrderPublic]
