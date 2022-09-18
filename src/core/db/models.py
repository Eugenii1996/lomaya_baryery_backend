import enum
import re
import uuid

from sqlalchemy import BIGINT, DATE, INTEGER, TIMESTAMP, Column, String, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import validates
from sqlalchemy.schema import ForeignKey


class RequestStatus(str, enum.Enum):
    APPROVED = "approved"
    DECLINED = "declined"
    PENDING = "pending"
    REPEAT_PENDING = "repeat pending"


class ShiftStatus(str, enum.Enum):
    STARTED = "started"
    FINISHED = "finished"
    PREPARING = "preparing"
    CANCELLED = "cancelled"


@as_declarative()
class Base:
    """Базовая модель."""
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_date = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_date = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp()
    )
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Shift(Base):
    """Смена."""
    status = Column(ENUM(Shift_statuses), nullable=False)
    started_at = Column(
        DATE, server_default=func.current_timestamp(), nullable=False
    )
    finished_at = Column(
        DATE, server_default=func.current_timestamp(), nullable=False
    )

    def __repr__(self):
        return f'<Shift: {self.id}, status: {self.status}>'


class User(Base):
    """Модель для пользователей"""
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    date_of_birth = Column(DATE, nullable=False)
    city = Column(String(50), nullable=False)
    phone_number = Column(BIGINT, unique=True, nullable=False)
    telegram_id = Column(INTEGER, unique=True, nullable=False)

    def __repr__(self):
        return f'<User: {self.id}, name: {self.name}, surname: {self.surname}>'

    @validates('name', 'surname')
    def validate_name_and_surname(self, key, value) -> str:
        regex = "^[a-zа-яё ]+$"
        if re.compile(regex).search(value.lower()) is None:
            raise ValueError('Фамилия или имя не корректные')
        if len(value) < 2:
            raise ValueError('Фамилия и имя должны быть больше 2 символов')
        return value.title()

    @validates('city')
    def validate_city(self, key, value) -> str:
        regex = "^[a-zA-Zа-яА-ЯёЁ -]+$"
        if re.compile(regex).search(value) is None:
            raise ValueError('Название города не корректное')
        if len(value) < 2:
            raise ValueError('Название города слишком короткое')
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value) -> str:
        if len(str(value)) != 11:
            raise ValueError('Поле телефона должно состоять из 11 цифр')
        return value


class Request(Base):
    """Модель рассмотрения заявок"""
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False
    )
    shift_id = Column(
        UUID(as_uuid=True), ForeignKey("shift.id"), nullable=False
    )
    status = Column(
        ENUM(Request_statuses),
        nullable=False,
        default=Request_statuses.PENDING
    )

    def __repr__(self):
        return f'<Request: {self.id}, status: {self.status}>'
