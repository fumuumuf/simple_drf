from rest_framework import serializers
from rest_framework.serializers import Serializer
import copy

from articles.models import Article, Category, Tag


class PKWritableMixin:
    """
    ModelSerializer を継承したフィールドを,
    更新系アクションのときは ID(PrimaryKeyRelatedField)で更新可能とする Mixin
    """

    def __init__(self, *args, **kwargs):
        self._org_pk_fields = {}
        super(PKWritableMixin, self).__init__(*args, **kwargs)

    def _get_pk_field(self, field: serializers.ModelSerializer, many=False):
        """
        field(ModelSerializerの) をもとに更新用の PrimaryKeyRelatedField を生成
        """

        attrs = {}

        # もとのフィールド定義をコピー
        for attr in [
            'required', 'default', 'allow_null',
            'validators', 'queryset', 'help_text', 'source'
        ]:
            if hasattr(field, attr):
                attrs[attr] = getattr(field, attr)

        return serializers.PrimaryKeyRelatedField(queryset=field.Meta.model._default_manager.all(), many=many,
                                                  **attrs)

    def get_fields(self):

        fields = super(PKWritableMixin, self).get_fields()
        if getattr(self.context.get('view'), 'action', '') not in ('create', 'update', 'partial_update',):
            return fields

        for f in [f for f in fields if not getattr(fields[f], 'read_only', True)]:

            if isinstance(fields[f], serializers.ListSerializer):
                target_serializer = fields[f].child
                many = True
            else:
                target_serializer = fields[f]
                many = False

            if isinstance(target_serializer, serializers.ModelSerializer):
                new_field = self._get_pk_field(target_serializer, many=many)
                self._org_pk_fields[f] = fields[f]
                fields[f] = new_field

        return fields

    def to_representation(self, obj):
        res = super(PKWritableMixin, self).to_representation(obj)

        # 変更したフィールドはもとの serializer でレンダリング
        for f, _serializer in self._org_pk_fields.items():
            if f not in self.fields:
                continue

            source = getattr(self.fields[f], 'source') or f
            if f in res and \
                    getattr(obj, source) is not None:
                res[f] = _serializer.to_representation(getattr(obj, source))
        return res


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ArticleSerializer(PKWritableMixin, serializers.ModelSerializer):
    # category = CategorySerializer(required=False, help_text='spam')
    category = CategorySerializer(required=False, help_text='spam')
    foos = TagSerializer(many=True, required=False, help_text='spam', source='tags')

    class Meta:
        model = Article
        # exclude = ('category',)
        fields = '__all__'
