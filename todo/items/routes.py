from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from bson import ObjectId

from ..users.routes import fastapi_users
from ..users.models import User, UserModel
from ..db import engine
from .models import Item

router = APIRouter(
    prefix='/items',
    tags=['items']
)


async def get_active_user(
        user: User = Depends(fastapi_users.current_user(active=True))):
    user_db = await UserModel.objects.get(id=user.id)
    return user_db


@router.get('', response_model=List[Item])
async def list_items(user: UserModel = Depends(get_active_user)):
    return await engine.find(Item, Item.user == user.id)


@router.get('/{id}', response_model=Item)
async def get_item(id: str, user: UserModel = Depends(get_active_user)):
    item = await engine.find_one(Item, (Item.id == ObjectId(id)) & (Item.user == user.id))

    if item:
        return item

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail='Item not found.')


@router.post('', response_model=Item)
async def add_or_update_item(
        item: Item,
        user: UserModel = Depends(get_active_user)):
    item.user = user.id
    return await engine.save(item)


@router.delete('/{id}')
async def delete_item(id: str, user: UserModel = Depends(get_active_user)):
    item = await engine.find_one(Item, (Item.id == ObjectId(id)) & (Item.user == user.id))

    if item:
        await engine.delete(item)
        return {'detail': 'Item deleted.'}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail='Item not found.')
