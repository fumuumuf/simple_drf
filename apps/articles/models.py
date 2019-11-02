from django.db import models
from django.db.models import Max

from accounts.models import User


class Tag(models.Model):
    name = models.CharField('タグ名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'


class Category(models.Model):
    name = models.CharField('name', max_length=120, default='no title')


class Article(models.Model):
    '''
    記事
    '''

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='記事の作者')
    title = models.CharField('タイトル', max_length=120, default='no title')
    body = models.TextField('本文')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='タグ', help_text='記事につけるタグ')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None, )

    def __str__(self):
        return f'{self.id} - {self.title}'

    class Meta:
        ordering = ['-created_at']


from django.db import models


class FFMManager(models.Manager):
    def add_root(self, **kwargs):
        """
        ルートの追加
        Args:
            **kwargs:
        Returns:
            FFM: 追加ノード
        """
        res = self.get_queryset().aggregate(val=Max('queue'))
        kwargs['queue'] = res['val'] or 0
        kwargs['depth'] = 0
        return self.create(**kwargs)


class FFM(models.Model):
    objects = FFMManager()
    depth = models.PositiveIntegerField()
    queue = models.PositiveIntegerField()
    name = models.CharField(max_length=100, blank=True, )
