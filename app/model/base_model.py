from datetime import datetime, timezone
from typing import Annotated

from sqlalchemy import func, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), server_default=func.now())]


class BaseModel(Base):
    __abstract__ = True
    id: Mapped[intpk]
    created_at: Mapped[created_at]
    updated_at: Mapped[created_at]


