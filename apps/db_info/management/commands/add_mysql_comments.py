import re

from django.core.management.base import AppCommand
from django.db import connections


class Command(AppCommand):
    help = 'add mysql comments'

    cursor = None

    def alter_table_comment(self, model):
        meta = model._meta
        statement = f"ALTER TABLE {meta.db_table} COMMENT '{meta.verbose_name}';"
        # statements.append(statement)
        self.cursor.execute(statement)
        return statement

    def _get_alter_column_statements_without_comment(self, table_name) -> dict:

        self.cursor.execute(f'SHOW CREATE TABLE {table_name}')
        f = self.cursor.fetchone()
        sql = f[1]
        lines = re.split(r'[\r\n]+', sql)
        columns = {}

        for line in lines:
            line = line.strip()
            m = re.match(r'^`(.*?)`.*', line)
            if not m: continue
            column_name = m.group(1)

            # 既存コメント除外
            s = re.sub(r"COMMENT +'([^']|'')+'[ ,]?", '', line)
            columns[column_name] = s[:-1]  # trim last `,`

        res = {}
        for k, v in columns.items():
            res[k] = f'alter table `{table_name}` modify {v} '
        return res

    def alter_columns_comment(self, model):
        meta = model._meta
        table_name = meta.db_table
        alter_statements = self._get_alter_column_statements_without_comment(table_name)

        statements = []

        for field in model._meta.fields:
            column = field.db_column or field.column
            statement = alter_statements.get(column, None)
            if not statement: continue

            comment = field.verbose_name
            if comment:
                statement += f" COMMENT '{comment}'"
                self.cursor.execute(statement)
                statements.append(statement)

        return statements

    def handle_app_config(self, app_config, **options):
        """
        # TODO: database を指定(今 default 固定)
        # TODO: 除外モデルを指定
        """

        if app_config.models_module is None:
            return

        connection = connections['default']
        self.cursor = connection.cursor()
        models = app_config.get_models(include_auto_created=True)

        statements = []
        for model in models:
            statements.append(self.alter_table_comment(model))
            statements += self.alter_columns_comment(model)

        connection.close()  # 必要？

        return '\n'.join(statements)
