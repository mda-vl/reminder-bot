from datetime import datetime
import requests
from loguru import logger

from pydantic import (
    BaseModel,
    constr,
    ValidationError,
    validator,
)
from sqlalchemy import (
    String,
    DateTime,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from utils import states


class Base(DeclarativeBase):
    pass


class AlarmSetORM(Base):
    __tablename__ = "alarm_set"

    _id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str | None] = mapped_column(String(50), nullable=True)
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    id: Mapped[int] = mapped_column(index=True)
    symbol: Mapped[str]
    price: Mapped[float]
    is_done: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )
    done_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, onupdate=datetime.now
    )


class AlarmSetModel(BaseModel):
    _id: int
    username: constr(max_length=50) | None = ""
    first_name: constr(max_length=50) | None = ""
    last_name: constr(max_length=50) | None = ""
    id: int
    symbol: constr(to_upper=True)
    price: float
    is_done: bool = False
    created_at: datetime | None
    done_at: datetime | None

    @validator("symbol")
    def test_symbol(cls, v: str) -> str:
        test_uri = f"{states.base_uri}klines?symbol={v}&interval=1h&limit=1"

        try:
            response = requests.get(test_uri, headers=states.headers)
            if response.status_code == 200:
                return v
            else:
                logger.error("Ошибка валидации торговой пары.")
                raise ValidationError

        except Exception:
            logger.error("Ошибка запроса к серверу Binance API.")
            raise Exception

    class Config:
        orm_mode = True
