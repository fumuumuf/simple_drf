from django.db import models

# Create your models here.
from tenant_schemas.models import TenantMixin


class Tenant(TenantMixin):
    name = models.CharField(max_length=128)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True
