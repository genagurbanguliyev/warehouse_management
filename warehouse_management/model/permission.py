from sqlalchemy import Enum, String

from sqlalchemy.orm import Mapped, mapped_column, relationship

from warehouse_management.enum.permission_enum import PermissionEnum
from warehouse_management.model.base_model import BaseModel


class PermissionModel(BaseModel):
    __tablename__ = "permissions"

    name: Mapped[str] = mapped_column(String, nullable=False)
    permission: Mapped[PermissionEnum] = mapped_column(Enum(PermissionEnum), unique=True, nullable=False)

    roles: Mapped[list["RoleModel"]] = relationship(
        "RoleModel", back_populates="permissions", secondary="role_permissions", lazy="selectin"
    )