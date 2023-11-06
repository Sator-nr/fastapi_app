from fastapi import FastAPI
from src.users.router import router as router_users
from src.bookings.routers import router as router_bookings
from src.hotels.router import router as router_hotels
from src.hotels.rooms.router import router as router_rooms


app = FastAPI()
app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
