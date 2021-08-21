import sqlalchemy
import databases
from ormar import ModelMeta
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from .config import settings

# SQL
database = databases.Database(settings.POSTGRES_DB_URL)
metadata = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


# NoSQL
client = AsyncIOMotorClient(settings.MONGODB_URL)
engine = AIOEngine(motor_client=client, database=settings.MONGO_DB)
