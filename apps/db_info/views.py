import os
import subprocess
import tempfile
from typing import List

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.files import File
from django.core.management import call_command
from django.http import HttpResponse
from django.views import View


class TableView(View):
    tmp_dir = None

    # TODO: 出力関連のコードを別モジュールに移動
    def get_target_app_configs(self) -> List[AppConfig]:
        targets = ['users', 'articles']
        return [config for config in apps.app_configs.values() if config.name in targets]

    def get_style_file(self):
        return os.path.join(settings.STATIC_ROOT, 'db_info/style.xsl')

    def get_target_tables(self) -> List[str]:
        """
        app 内のすべてのモデルの table を取得
        """

        configs = self.get_target_app_configs()
        tables = []
        for app_config in configs:
            for model_name, model in app_config.models.items():
                tables.append(model._meta.db_table)
        return tables

    def output_table_info_from_mysql(self) -> str:
        """
        mysqldump を使ってテーブル定義の xml ファイルを出力

        Returns: file name
        """
        db_info = settings.DATABASES['default']
        cmd_params = [
            'mysqldump',
            '--no-data',
            '--xml',
            f'--user={db_info["USER"]}',
            f'--password={db_info["PASSWORD"]}',
            f'--host={db_info["HOST"]}',
            db_info['NAME'],
            '--tables',
        ]
        cmd_params += self.get_target_tables()
        file_name = os.path.join(self.tmp_dir, 'spam.xml')
        with open(file_name, 'wb') as f:
            popen = subprocess.Popen(cmd_params, stdout=f)
        popen.wait()

        return file_name

    def run_convert_xml_to_html(self, xml_path):
        html_path = os.path.join(self.tmp_dir, 'spam.html')
        cmd_params = [
            'xsltproc',
            '--output', html_path,
            self.get_style_file(),
            xml_path
        ]
        subprocess.run(cmd_params)
        return html_path

    def get_table_layout(self):
        xml_path = self.output_table_info_from_mysql()
        return self.run_convert_xml_to_html(xml_path)

    def get(self, request):
        with tempfile.TemporaryDirectory() as d:
            self.tmp_dir = d
            html_file = self.get_table_layout()
            response = HttpResponse(File(open(html_file, 'rb')), content_type='text/html')
            return response


class GraphModelsView(View):

    # TODO: 出力関連のコードを別モジュールに移動
    def get_target_app_names(self) -> List[str]:
        return ['accounts', 'articles']

    def get_options(self):
        return {
            'exclude_models': ['Permission', ],
            'exclude_columns': ['created_at', 'updated_at'],
            'verbose_names': True,
            'group_models': True,
            'disable_sort_fields': True,
        }

    def get(self, request):
        target_apps = self.get_target_app_names()
        with tempfile.TemporaryDirectory() as d:
            fpath = os.path.join(d, 'spam.pdf')
            kwargs = self.get_options()
            kwargs.update({
                'outputfile': fpath
            })
            call_command('graph_models', *target_apps, **kwargs)

            response = HttpResponse(File(open(fpath, 'rb')), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename=er-diagram.pdf'
            return response
