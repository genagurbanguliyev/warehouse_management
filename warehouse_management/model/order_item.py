from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

from warehouse_management.model import OrderModel, ProductModel
from warehouse_management.model.base_model import intpk, Base


class OrderItemModel(Base):
    __tablename__ = "order_item"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id', ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id', ondelete="CASCADE"), primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    # Back-references to parent Order and Product
    order: Mapped["OrderModel"] = relationship(
        "OrderModel",
        overlaps="orders,products"
    )

    product: Mapped["ProductModel"] = relationship(
        "ProductModel",
        overlaps="orders,products"
    )