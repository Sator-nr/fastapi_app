from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column(nullable=False)
    services: Mapped[Optional[list[str]]] = mapped_column(JSON)
    quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column()

    class Config:
        orm_mode = True
