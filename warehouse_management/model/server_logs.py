from sqlalchemy import Enum, Text, VARCHAR, String
from sqlalchemy.orm import Mapped, mapped_column

from warehouse_management.enum.log_status_enum import LogStatusEnum
from warehouse_management.model.base_model import BaseModel


class ServerLogsModel(BaseModel):
    __tablename__ = "server_logs"

    module: Mapped[str | None] = mapped_column(String, nullable=True)
    method: Mapped[str | None] = mapped_column(VARCHAR(100), nullable=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[LogStatusEnum] = mapped_column(Enum(LogStatusEnum), nullable=False)
    action: Mapped[str | None] = mapped_column(String, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(VARCHAR(100), nullable=True)
    user: Mapped[str | None] = mapped_column(String, nullable=True)
    body: Mapped[str | None] = mapped_column(String, nullable=True)
