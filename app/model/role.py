from sqlalchemy import String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.model.base_model import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    users: Mapped[list["UserModel"]] = relationship("UserModel", back_populates="role_detail", lazy="selectin")
    permissions: Mapped[list["PermissionModel"]] = relationship(
        "PermissionModel", back_populates="roles", secondary="role_permissions", lazy="selectin"
    )