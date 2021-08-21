from typing import Optional
from odmantic import Model
from uuid import UUID


class Item(Model):
    user: Optional[UUID]
    name: str
    done: bool = False

    class Config:
        schema_extra = {
            'example': {
                'name': 'Do what?'
            }
        }
