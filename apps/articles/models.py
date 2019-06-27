from django.db import models

from accounts.models import User
from softdelete.models import SoftDeleteObject


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Category(SoftDeleteObject):
    name = models.CharField('name', max_length=120, default='no title')


class Article(SoftDeleteObject):
    '''
    記事
    '''

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='記事の作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None, )
    title = models.CharField('タイトル', max_length=120, default='no title')
    body = models.TextField('本文')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='タグ', help_text='記事につけるタグ')

    def __str__(self):
        return f'{self.id} - {self.title}'


class Meta:
    ordering = ['-created_at']
