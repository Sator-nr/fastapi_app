from datetime import date

from fastapi import APIRouter
from fastapi.openapi.models import Response
from fastapi_cache.decorator import cache
from fastapi.requests import Request
from pydantic import parse_obj_as

from src.hotels.dao import HotelsDAO
from src.hotels.rooms.dao import RoomsDAO
from src.hotels.schemas import SHotelResponse

router = APIRouter(prefix="/hotels",
                   tags=['Отели и комнаты'])


@router.get("/{location}", response_model=list[SHotelResponse])
@cache(expire=30, namespace='hotels')
async def get_hotels(location: str, date_from: date, date_to: date):
    ret = []
    hotels = await HotelsDAO.find_all(location=location)
    for hotel in hotels:
        unoccupied_rooms = 0
        rooms = await RoomsDAO.find_all(hotel_id=hotel.id)
        for room in rooms:
            unoccupied_rooms += await RoomsDAO.unoccupied_left(room.id, date_from, date_to)
        hotel.unoccupied_rooms = unoccupied_rooms
        ret.append(hotel)
    # ret_parsed = parse_obj_as(list[SHotelResponse], ret) # Другой пример валидации
    return ret
