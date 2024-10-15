from typing import List

from sqlalchemy import Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from warehouse_management.model.base_model import Base, intpk


class ProductModel(Base):
    __tablename__ = "product"

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    desc: Mapped[str | None] = mapped_column(Text, nullable=True)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    orders: Mapped[List["OrderModel"]] = relationship(
        secondary="order_item",
        back_populates="products",
        lazy="selectin",
        overlaps="order"
    )
