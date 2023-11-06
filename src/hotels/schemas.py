from datetime import date
from typing import Optional
from fastapi import Query
from pydantic import BaseModel


class FindHotelResponse(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[list[str]]
    rooms_quantity: int
    image_id: int
    unoccupied_rooms: int

    class Config:
        # orm_mode = True
        from_attributes = True
