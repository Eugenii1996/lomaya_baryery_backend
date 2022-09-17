import re
import uuid

from sqlalchemy import func, Column, TIMESTAMP, DATE
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    """Базовая модель."""
    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at = Column(
        TIMESTAMP, server_default=func.current_timestamp(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp()
    )
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        class_name = cls.__name__
        split_name = re.sub("([A-Z])", r" \1", class_name).lower().split()
        return "_".join(split_name)


class Shift(Base):
    """Смена."""
    status_choices = ENUM(
        "started", "finished", "preparing", "cancelled", name="status_choice"
    )
    status = Column(status_choices, nullable=False)
    started_at = Column(
        DATE, server_default=func.current_timestamp(), nullable=False
    )
    finished_at = Column(DATE, nullable=False)

    def __repr__(self):
        return f'<Shift: {self.id}, status: {self.status}>'
