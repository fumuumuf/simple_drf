from django.contrib import admin

# Register your models here.
from articles.models import Article, Tag

admin.site.register(Article)
admin.site.register(Tag)
