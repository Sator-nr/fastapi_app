from datetime import date
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Computed


class SRoomResponse(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[list[str]]
    quantity: int
    image_id: int
    unoccupied: int
    total_cost: int

    class Config:
        # orm_mode = True
        from_attributes = True
