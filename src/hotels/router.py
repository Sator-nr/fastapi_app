from datetime import date

from fastapi import APIRouter

from src.hotels.dao import HotelsDAO
from src.hotels.rooms.dao import RoomsDAO
from src.hotels.schemas import FindHotelResponse

router = APIRouter(prefix="/hotels",
                   tags=['Отели и комнаты'])


@router.get("/{location}", response_model=list[FindHotelResponse])
async def get_hotels(location: str, date_from: date, date_to: date):
    response = []
    hotels = await HotelsDAO.find_all(location=location)
    for hotel in hotels:
        unoccupied_rooms = 0
        rooms = await RoomsDAO.find_all(hotel_id=hotel.id)
        for room in rooms:
            unoccupied_rooms += await RoomsDAO.unoccupied_left(room.id, date_from, date_to)
        hotel.unoccupied_rooms = unoccupied_rooms
        response.append(hotel)
    return response
