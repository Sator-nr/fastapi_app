from fastapi import APIRouter, Depends
from sqlalchemy import select
from starlette.requests import Request

from src.bookings.dao import BookingDAO
from src.bookings.models import Bookings
from src.bookings.schemas import SBooking
from src.database import async_session_maker
from src.users.models import Users
from src.users.dependencies import get_current_user

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирования']
)


@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)




