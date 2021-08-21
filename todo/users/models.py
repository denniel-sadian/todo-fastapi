from typing import Optional

import ormar
from fastapi_users import models
from fastapi_users.db import OrmarBaseUserModel, OrmarUserDatabase

from ..db import BaseMeta


class User(models.BaseUser):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(models.BaseUserCreate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(User, models.BaseUserUpdate):
    pass


class UserDB(User, models.BaseUserDB):
    pass


class UserModel(OrmarBaseUserModel):
    first_name = ormar.String(max_length=100, nullable=True)
    last_name = ormar.String(max_length=100, nullable=True)

    class Meta(BaseMeta):
        tablename = 'users'


user_db = OrmarUserDatabase(UserDB, UserModel)
