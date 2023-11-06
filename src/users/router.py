from fastapi import APIRouter, Depends
from fastapi import Response

from src.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dao import UsersDAO
from src.users.models import Users
from src.users.schemas import SUserAuth
from src.users.dependencies import get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['Auth & Users'],
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    return


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return


@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user
