from django.db import models
from django.db.models import QuerySet
from django.utils import timezone


class SoftDeletableQuerySet(QuerySet):
    def delete(self):
        """
        Soft delete objects from queryset (set their ``is_removed``
        field to True)
        """
        self.update(is_removed=True, deleted_at=timezone.now())


class SoftDeletableManager(models.Manager):
    _queryset_class = SoftDeletableQuerySet

    def get_queryset(self):
        """
        Return queryset limited to not removed entries.
        """
        kwargs = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):
            kwargs['hints'] = self._hints

        return self._queryset_class(**kwargs).filter(is_removed=False)
