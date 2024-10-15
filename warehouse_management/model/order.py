from typing import List

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from warehouse_management.enum.order_enum import OrderStatusEnum
from warehouse_management.model.base_model import BaseModel
from warehouse_management.model.product import ProductModel
from warehouse_management.model.user import UserModel


class OrderModel(BaseModel):
    __tablename__ = "order"

    delivery_address: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[OrderStatusEnum] = mapped_column(Enum(OrderStatusEnum), nullable=False)
    username: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE", onupdate="CASCADE"))

    user_detail: Mapped[UserModel] = relationship(
        "UserModel",
        primaryjoin='foreign(OrderModel.username) == UserModel.username',
        lazy="selectin",
        remote_side="UserModel.username"
    )

    products: Mapped[List["ProductModel"]] = relationship(
        secondary="order_item",
        back_populates="orders",
        lazy="selectin",
        overlaps="product, order"
    )