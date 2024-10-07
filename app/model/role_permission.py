from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.enum.permission_enum import PermissionEnum
from app.model.base_model import Base


class RolePermissionsModel(Base):
    __tablename__ = "role_permissions"

    role: Mapped[str] = mapped_column(ForeignKey("roles.role", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    permission: Mapped[PermissionEnum] = mapped_column(ForeignKey("permissions.permission", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
