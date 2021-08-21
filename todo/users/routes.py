from fastapi import APIRouter, Request
from fastapi_users.authentication import JWTAuthentication
from fastapi_users import FastAPIUsers

from ..config import settings
from .models import (
    User,
    UserCreate,
    UserUpdate,
    UserDB,
    user_db
)

jwt_authentication = JWTAuthentication(
    secret=settings.SECRET_KEY,
    lifetime_seconds=settings.TOKEN_EXPIRES_IN_SECONDS,
    tokenUrl='auth/jwt/login'
)

fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

router = APIRouter()


def on_after_register(user: UserDB, request: Request):
    print(f'User {user.id} has registered.')


def on_after_forgot_password(user: UserDB, token: str, request: Request):
    print(f'User {user.id} has forgot their password. Reset token: {token}')


def after_verification_request(user: UserDB, token: str, request: Request):
    print(
        f'Verification requested for user {user.id}. Verification token: {token}')


router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix='/auth/jwt', tags=['auth']
)
router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix='/auth', tags=['auth']
)
router.include_router(
    fastapi_users.get_reset_password_router(
        settings.SECRET_KEY, after_forgot_password=on_after_forgot_password
    ),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_verify_router(
        settings.SECRET_KEY, after_verification_request=after_verification_request
    ),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(fastapi_users.get_users_router(),
                      prefix='/users', tags=['users'])
