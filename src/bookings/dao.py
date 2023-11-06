from datetime import date
from sqlalchemy import select, and_, or_, func, insert, delete

from src.bookings.models import Bookings
from src.dao.base import BaseDAO
from src.database import engine, async_session_maker
from src.exceptions import NoBookingException
from src.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from
                        )
                    )
                )
            ).cte("booked_rooms")
            get_rooms_left = select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label('rooms_left')
                ).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == room_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )
            # print(get_rooms_left.compile(engine, compile_kwargs={'literal_binds': True}))
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()
            # print(rooms_left)
            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(Bookings)
                mew_booking = await session.execute(add_booking)
                await session.commit()
                return mew_booking.scalar()
            else:
                return None

    @classmethod
    async def delete(
            cls,
            user_id: int,
            booking_id: int):
        async with async_session_maker() as session:
            statement = delete(Bookings).where(Bookings.id == booking_id, Bookings.user_id == user_id)
            result = await session.execute(statement)
            await session.commit()
            if result.rowcount == 0:
                raise NoBookingException

