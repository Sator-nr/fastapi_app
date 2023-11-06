from datetime import date

from sqlalchemy import select, and_, or_, func

from src.bookings.models import Bookings
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels



