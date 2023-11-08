from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from contextlib import asynccontextmanager

from src.users.router import router as router_users
from src.bookings.routers import router as router_bookings
from src.hotels.router import router as router_hotels
from src.hotels.rooms.router import router as router_rooms
from src.pages.router import router as router_pages
from src.images.router import router as router_images
from src.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-app")
    # logger.info("Service started")
    print('Сервис запущен')
    yield
    # logger.info("Service exited")
    print('Сервис завершен')


app = FastAPI(lifespan=lifespan)

app.mount('/static', StaticFiles(directory="src/static"), 'static')

app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_pages)
app.include_router(router_images)

origins = [
    'http://localhost:8000/'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['Content-Type', 'Set-Cookie', 'Access-Control-Allow-Headers',
                   'Access-Control-Allow-Origin', 'Authorization']
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-app")
