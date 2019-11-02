from django.contrib import admin

# Register your models here.
from articles.models import Article, Tag, Category, FertileForestNode

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(FertileForestNode)

