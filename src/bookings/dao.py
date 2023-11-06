from src.bookings.models import Bookings
from src.dao.base import BaseDAO


class BookingDAO(BaseDAO):
    model = Bookings

