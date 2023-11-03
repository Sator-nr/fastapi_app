from sqlalchemy import Column, Integer, String

from src.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    hashed_password = Column(String)

    class Config:
        orm_mode = True
