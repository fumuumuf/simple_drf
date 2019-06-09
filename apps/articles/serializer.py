from rest_framework import serializers
from rest_framework.serializers import Serializer
import copy

from articles.models import Article, Category


class PKWritableMixin:

    def __init__(self, *args, **kwargs):
        self.org_pk_fields = {}
        super(PKWritableMixin, self).__init__(*args, **kwargs)

    def exchange_pk_field(self, fields, name):
        field = fields[name]
        attrs = {}

        # もとのフィールド定義をコピー
        for attr in [
            'required', 'default', 'allow_null',
            'validators', 'queryset', 'help_text', 'source'
        ]:
            if hasattr(field, attr):
                attrs[attr] = getattr(field, attr)

        new_field = serializers.PrimaryKeyRelatedField(queryset=field.Meta.model._default_manager.all(),
                                                       **attrs)
        self.org_pk_fields[name] = field
        fields[name] = new_field

    def get_fields(self):

        fields = super(PKWritableMixin, self).get_fields()
        if getattr(self.context.get('view'), 'action', '') not in ('create', 'update', 'partial_update',):
            return fields

        for f in [f for f in fields \
                  if isinstance(fields[f], serializers.ModelSerializer)]:
            if getattr(fields[f], 'read_only', True): continue

            self.exchange_pk_field(fields, f)

        return fields

    def to_representation(self, obj):
        res = super(PKWritableMixin, self).to_representation(obj)

        # 変更したフィールドはもとの serializer でレンダリング
        for f, _serializer in self.org_pk_fields.items():
            source = getattr(self.fields[f], 'source') or f
            if f in res:
                attr_val = getattr(obj, source)
                if attr_val:
                    res[f] = _serializer.to_representation(getattr(obj, source))
        return res



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(PKWritableMixin, serializers.ModelSerializer):
    # category = CategorySerializer(required=False, help_text='spam')
    alter_category = CategorySerializer(required=False, help_text='spam', source='category')

    class Meta:
        model = Article
        exclude = ('category',)
        # fields = '__all__'
