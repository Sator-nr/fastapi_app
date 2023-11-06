from fastapi import APIRouter
from sqlalchemy import select

from src.bookings.dao import BookingDAO
from src.bookings.models import Bookings
from src.bookings.schemas import SBooking
from src.database import async_session_maker

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()




