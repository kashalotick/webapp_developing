from datetime import datetime, timedelta
from typing import TYPE_CHECKING

from sqlalchemy import String, Interval, DateTime
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.db import Base


class UserModel(Base):
    __tablename__ = "races"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)