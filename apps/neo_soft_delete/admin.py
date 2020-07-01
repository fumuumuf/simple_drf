from django.contrib import admin


class AllSoftDeleteObjectAdmin(admin.ModelAdmin):
    """
    soft delete されたオブジェクトも監視する ModelAdmin
    """

    def get_queryset(self, request):
        try:
            qs = self.model.all_objects.all()
            print(qs)
        except Exception:
            qs = self.model._default_manager.all()

        ordering = self.get_ordering(request) or ()
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        self.get_queryset(request).filter(pk=obj.pk).delete()


class SoftDeleteObjectAdmin(admin.ModelAdmin):
    """
    soft delete されたオブジェクトを表示しない ModelAdmin
    """
    delete_confirmation_template = 'admin/softdelete/delete_confirmation.html'

    # delete_selected_confirmation_template ='admin/softdelete/delete_selected_confirmation.html'

    def get_fields(self, *args, **kwargs):
        res = super(SoftDeleteObjectAdmin, self).get_fields(*args, **kwargs)
        if 'is_removed' in res:
            res = [v for v in res if v != 'is_removed']
        return res


from django.contrib import admin

# Register your models here.
from .models import Item, SubItem, SubItemNoSoftDelete, ItemType, ItemTypeRelation

admin.site.register(Item, SoftDeleteObjectAdmin)
admin.site.register(SubItem, SoftDeleteObjectAdmin)
admin.site.register(SubItemNoSoftDelete)
admin.site.register(ItemType, SoftDeleteObjectAdmin)
admin.site.register(ItemTypeRelation)
