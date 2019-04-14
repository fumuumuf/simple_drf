from django.core.management.commands.migrate import Command as MigrationCommand

from django.db import connection
from ...utils import get_tenants_map


class Command(MigrationCommand):
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            schemas = get_tenants_map().values()
            for schema in schemas:
                # scheme 作成
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {schema}")

                # scheme 切り替え
                cursor.execute(f"USE {schema}")
                super(Command, self).handle(*args, **options)
