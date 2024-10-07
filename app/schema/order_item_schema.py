from pydantic import BaseModel


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int


class OrderItemPublic(OrderItemSchema):
    id: int
    order_id: int
