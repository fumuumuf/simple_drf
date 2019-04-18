#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import dotenv

dotenv.load_dotenv()

from simple_drf.middleware import set_db_for_router


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_drf.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.runserver import Command as runserver
        runserver.default_addr = "0.0.0.0"
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    from django.db import connection

    args = sys.argv
    db = args[1]
    with connection.cursor() as cursor:
        set_db_for_router(db)
        del args[1]
        print(args)
        execute_from_command_line(args)


if __name__ == '__main__':
    main()
