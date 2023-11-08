from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from src.bookings.dao import BookingDAO
from src.bookings.schemas import SBooking
from src.exceptions import RoomCanNotBeBooked
from src.hotels.rooms.dao import RoomsDAO
from src.tasks.tasks import send_booking_confirmation_email
from src.users.models import Users
from src.users.dependencies import get_current_user

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get("", response_model=list[SBooking])
async def get_bookings(user: Users = Depends(get_current_user)):
    bookings = await BookingDAO.find_all(user_id=user.id)
    for booking in bookings:
        room = await RoomsDAO.find_by_id(booking.room_id)
        booking.image_id = room.image_id
        booking.name = room.name
        booking.description = room.description
        booking.services = room.services
    return bookings


@router.post("")
async def add_booking(room_id: int,
                      date_from: date,
                      date_to: date,
                      user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBooked
    # Костыль, не хочу менять схему
    booking.image_id = 0
    booking.name = ''
    booking.description = ''
    booking.services = []
    # # #
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking_dict


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    return await BookingDAO.delete(user.id, booking_id)




