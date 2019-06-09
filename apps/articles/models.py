from django.db import models

from accounts.models import User


class Category(models.Model):
    name = models.CharField('カテゴリ名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Article(models.Model):
    '''
    記事
    '''

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='記事の作者')
    title = models.CharField('タイトル', max_length=120, default='no title')
    body = models.TextField('本文')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name='articles', verbose_name='category')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='タグ', help_text='記事につけるタグ')

    def __str__(self):
        return f'{self.id} - {self.title}'


class Meta:
    ordering = ['-created_at']
