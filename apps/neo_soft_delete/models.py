from django.db import models
# Create your models here.
from model_utils.fields import MonitorField
from model_utils.models import SoftDeletableModel as DefaultSoftDeletableModel

from neo_soft_delete.managers import SoftDeletableManager


class SoftDeletableModel(DefaultSoftDeletableModel):
    objects = SoftDeletableManager()

    deleted_at = MonitorField(monitor='is_removed', when=[True], null=True, default=None, editable=False)

    class Meta:
        abstract = True

class Item(SoftDeletableModel):
    name = models.CharField('name', max_length=120, default='no title')


class SubItem(SoftDeletableModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField('name', max_length=120, default='no title')


class SubItemNoSoftDelete(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    name = models.CharField('name', max_length=120, default='no title')


class ItemType(SoftDeletableModel):
    """
    アイテム種類のモデル
    """
    name = models.CharField('名前', max_length=1000, blank=True)

    class Meta:
        verbose_name = 'アイテム種類'
        verbose_name_plural = 'アイテム種類'


class ItemTypeRelation(models.Model):
    """プランとアイテム種類の中間テーブル"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='item_type_relations')
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE)
