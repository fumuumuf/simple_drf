from django.contrib import admin

from articles.models import Article, Tag, Category
# Register your models here.
from softdelete.admin import SoftDeleteObjectAdmin

admin.site.register(Article, SoftDeleteObjectAdmin)
admin.site.register(Category, SoftDeleteObjectAdmin)
admin.site.register(Tag)
