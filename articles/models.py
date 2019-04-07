from django.db import models
from django_currentuser.middleware import get_current_authenticated_user

from accounts.models import User

# As model field:
from django_currentuser.db.models import CurrentUserField


class Foo(models.Model):
    created_by = CurrentUserField()


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
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='タグ', help_text='記事につけるタグ')

    created_by = CurrentUserField(verbose_name='作成者', editable=False, related_name='create_articles')
    updated_by = CurrentUserField(verbose_name='更新者', editable=False, related_name='update_articles')

    def save(self, *args, **kwargs):
        self.updated_by = get_current_authenticated_user()
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id} - {self.title}'


class Meta:
    ordering = ['-created_at']
