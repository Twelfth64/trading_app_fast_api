import datetime

from sqlalchemy.orm import Mapped, mapped_column

from src.auth.models import Base


class OperationOrm(Base):
    __tablename__ = 'operation'

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    figi: Mapped[str]
    instrument_type: Mapped[str] = mapped_column(nullable=True)
    date: Mapped[datetime.datetime]
    type: Mapped[str]
