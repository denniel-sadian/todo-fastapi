import sys
from datetime import datetime
from asyncio import run

from uvicorn import run
from alembic import config

from todo.config import settings


if __name__ == '__main__':
    command = sys.argv[1:]

    # Run the app.
    if command[0] == 'rundev':
        app = settings.APP
        port = int(command[1]) if len(command) == 2 else settings.PORT
        reload_dirs = [app.split('.')[0]]
        run(app, port=port, host='0.0.0.0', reload=True, reload_dirs=reload_dirs)

    # Make migrations.
    elif command[0] == 'makemigrations':
        date_comment = str(datetime.now()).split('.')[0]
        date_comment = date_comment.replace('-', '_')
        date_comment = date_comment.replace(' ', '_')
        date_comment = date_comment.replace(':', '_')
        alembic_args = ['revision', '--autogenerate', '-m', date_comment]
        config.main(argv=alembic_args)

    # Migrate.
    elif command[0] == 'migrate':
        config.main(argv=['--raiseerr', 'upgrade', 'head'])
