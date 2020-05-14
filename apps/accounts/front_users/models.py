from django.db import models

# Create your models here.
from accounts.models import User


class TenantUser(User):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        parent_link=True,
        related_name='tenant_user',
    )

    name = models.CharField('お名前', max_length=150, blank=True)
    kana = models.CharField('ふりがな', max_length=150, blank=True)
