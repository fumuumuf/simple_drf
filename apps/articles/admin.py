import tempfile

from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin
from import_export.admin import ExportMixin, ImportExportModelAdmin
from import_export.formats.base_formats import CSV
from import_export.tmp_storages import TempFolderStorage

from articles.models import Article, Tag, Category

admin.site.register(Tag)
admin.site.register(Category)

from import_export import resources


class ArticleResource(resources.ModelResource):
    class Meta:
        model = Article

    def import_data(self, dataset, *args, **kwargs):
        dataset.headers= ['id', 'title', ]
        return super(ArticleResource, self).import_data(dataset,*args,**kwargs)


class SJIS_CSV(CSV):
    """
    CSV を shift_jis で出力するための Format class
    """
    CONTENT_TYPE = 'text/csv; charset=shift_jis'


class ShiftJISTempFolderStorage(TempFolderStorage):
    def open(self, mode='r'):
        if self.name:
            return open(self.get_full_path(), mode, encoding='shift_jis')
        else:
            tmp_file = tempfile.NamedTemporaryFile(delete=False)
            self.name = tmp_file.name
            return tmp_file


class ShiftJISCSVImportExportMixin:
    """
    encoding:shift_jis の CSV を import/export する場合はこの mixin を継承してください
    """
    formats = [SJIS_CSV]
    from_encoding = "shift_jis"
    tmp_storage_class = ShiftJISTempFolderStorage


class ArticleAdmin(ShiftJISCSVImportExportMixin,ImportExportModelAdmin):
    resource_class = ArticleResource


admin.site.register(Article, ArticleAdmin)
