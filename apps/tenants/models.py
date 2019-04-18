from django.db import models

# Create your models here.
class Tenant(models.Model):
    name = models.CharField('店舗名', max_length=120)

    def __str__(self):
        return f'{self.id} - {self.name}'
