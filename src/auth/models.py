import datetime

from typing import Annotated

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Column,
    ForeignKey,
    text,
    JSON
)

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]


class Base(DeclarativeBase):
    pass


class RoleOrm(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    permissions = Column(JSON) # TODO: add permissions


class UserOrm(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    registered_at: Mapped[created_at]
    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"))
