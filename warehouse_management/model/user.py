from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from warehouse_management.model.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(ForeignKey("roles.role", ondelete="CASCADE", onupdate="CASCADE"))

    role_detail: Mapped["RoleModel"] = relationship("RoleModel", back_populates="users", lazy="joined")
    orders: Mapped[list["OrderModel"]] = relationship(
        "OrderModel",
        back_populates="user_detail",
        primaryjoin='UserModel.username == foreign(OrderModel.username)',
        lazy="selectin"
    )
