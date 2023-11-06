from datetime import date

from src.hotels.rooms.dao import RoomsDAO
from src.hotels.router import router


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    response = []
    rooms = await RoomsDAO.find_all(hotel_id=hotel_id)
    for room in rooms:
        unoccupied_left = await RoomsDAO.unoccupied_left(room.id, date_from, date_to)
        room.unoccupied_rooms = unoccupied_left
        room.total_cost = (date_to - date_from).days * room.price
        response.append(room)
    return response
