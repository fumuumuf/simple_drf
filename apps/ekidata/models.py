from django.db import models

# Create your models here.

E_STATUS = ((0, '運用中'), (1, '運用前'), (2, '廃止'))


class Line(models.Model):
    id = models.IntegerField('路線コード', primary_key=True, db_column='line_cd')
    name = models.CharField('路線名称(一般)', max_length=128, db_column='line_name')
    line_name_k = models.CharField('路線名称(一般・カナ)', max_length=128, null=True, blank=True)
    line_name_h = models.CharField('路線名称(正式名称)', max_length=128, null=True, blank=True)
    lat = models.DecimalField('路線表示時の中央緯度', max_digits=9, decimal_places=6, default=None, null=True)
    lon = models.DecimalField('路線表示時の中央経度', max_digits=9, decimal_places=6, default=None, null=True)

    e_status = models.IntegerField('状態', choices=E_STATUS, null=True, default=None)

    zoom = models.IntegerField('路線表示時のGoogleMap倍率', null=True)
    e_sort = models.IntegerField('並び順', null=True, default=None)

    class Meta:
        verbose_name = '路線'
        verbose_name_plural = '路線'


class Station(models.Model):
    id = models.IntegerField('駅コード', primary_key=True, db_column='station_cd')
    station_g_cd = models.CharField('名称', max_length=128, db_column='station_name')
    name = models.CharField('名称', max_length=128, db_column='station_name')

    line = models.ForeignKey(Line, on_delete=models.CASCADE, db_column='line_cd')
    prefecture = models.IntegerField('都道府県', db_column='pref_cd', null=True, default=None)

    post = models.CharField('駅郵便番号', max_length=128, null=True, default=None)
    add = models.CharField('住所', max_length=300, null=True, default=None)

    lat = models.DecimalField('緯度', max_digits=9, decimal_places=6, default=None, null=True)
    lon = models.DecimalField('経度', max_digits=9, decimal_places=6, default=None, null=True)

    open_ymd = models.DateField('開業年月日', null=True, default=None)
    close_ymd = models.DateField('廃止年月日', null=True, default=None)
    e_status = models.IntegerField('状態', choices=E_STATUS, null=True, default=None)
    e_sort = models.IntegerField('並び順', null=True, default=None)

    class Meta:
        verbose_name = '駅'
        verbose_name_plural = '駅'
