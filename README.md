# todo-app-fastapi

A simple async todo app using `fastapi`, `fastapi-users`, `ormar` and `alembic`, and `odmantic`. For experimentation, this uses postgresql and mongodb.


## Run with Docker
```
docker-compose up -d --build
docker-compose exec python manage.py migrate
```



## Running with just a virtual env
```
mkdir todo_fastapi
cd todo_fastapi
git clone https://github.com/denniel-sadian/todo-app-fastapi.git .
python -m venv env
# Windows
./env/Scripts/activate
# Linux
source ./env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py rundev
```

You can visit the api at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



## When you make some changes with the sql models
1. `python manage.py makemigrations`
2. `python manage.py migrate`

There is no migration system for the nosql part.

## Making new sql models discoverable
The structure of this app is this:
```
todo_fastapi                              # The whole project directory.
|
|---- migrations                          # This is for the migrations.
|     |---- versions                      # The actual migration files are here.
|     |---- env.py                        # The `metadata` obj from `db.py`, and the models are imported here. 
|     |---- README.md
|     `---- script.py.mako                # This is the template used for making migration py files.
|
|---- todo                                # This is the main dir of the sub apps.
|     |---- items                         # This is a sub app.
|     |     |---- __init__.py
|     |     |---- models.py               # ORM models and schemas are here.
|     |     `---- routes.py               # The routes of items sub app are here.
|     |
|     |---- users
|     |     |---- __init__.py
|     |     |---- models.py               # ORM models and schemas are here.
|     |     `---- routes.py               # The routes of users sub app are here.
|     |
|     |---- __init__.py
|     |---- db.py                         # This contains the `metadata` and `BaseMeta` class.
|     |---- main.py                       # The main app where the `FastAPI` class is instantiated.
|     `---- settings.py                   # The settings are here.
|
|
|---- .gitignore
|---- alembic.ini                         # This is the alembic config file, it's always overriden by the `env.py`.
|---- manage.py                           # This is a simple script inspired by Django.
|---- README.md
`---- requirements.txt
```
You edit the `env.py` and import all of your sql models there.

For example:
```
...
# Import models here so alembic can see them.
from todo.users.models import *
...
```

#### What Alembic detects from sql models:
- Table additions, removals.
- Column additions, removals.
- Change of nullable status on columns.
- Basic changes in indexes and explicitly-named unique constraints.
- Basic changes in foreign key constraints.

You can find more about [what alembic can and cannot autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html#what-does-autogenerate-detect-and-what-does-it-not-detect).


#### Used libraries besides from FastAPI
- [fastapi-users](https://github.com/frankie567/fastapi-users) for authentication with JWT.
- [ormar](https://github.com/collerek/ormar) for the sql database part.
- [alembic](https://github.com/sqlalchemy/alembic) for the database migrations.
- [odmantic](https://github.com/art049/odmantic) for the nosql database part.
