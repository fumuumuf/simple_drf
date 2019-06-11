from rest_framework import serializers

from articles.models import Article, Category, Tag


class PKWritableMixin:
    """
    ModelSerializer を継承したフィールドに対し
    更新系アクションのときは id(PrimaryKeyRelatedField)で更新可能とする Mixin
    """

    def __init__(self, *args, **kwargs):
        self._org_pk_fields = {}
        super(PKWritableMixin, self).__init__(*args, **kwargs)

    def _get_pk_field(self, field, queryset):
        """
        ModelSerializer の更新用の PrimaryKeyRelatedField を返します.
        対象フィールドが ModelSerializer でない場合は None を返します.
        """

        attrs = {}
        if isinstance(field, serializers.ListSerializer):
            serializer = field.child
            attrs['many'] = True
            attrs['source'] = field.source
        elif isinstance(field, serializers.ModelSerializer):
            serializer = field
        else:
            return None

        attrs['queryset'] = queryset if queryset is not None else serializer.Meta.model._default_manager.all()

        # もとのフィールド定義をコピー (HACK: プロパティの過不足検証)
        for attr in [
            'required', 'default', 'allow_null',
            'validators', 'queryset', 'help_text', 'source'
        ]:
            if hasattr(serializer, attr) and attr not in attrs:
                attrs[attr] = getattr(serializer, attr)

        return serializers.PrimaryKeyRelatedField(**attrs)

    def get_fields(self):

        fields = super(PKWritableMixin, self).get_fields()
        if getattr(self.context.get('view'), 'action', '') not in ('create', 'update', 'partial_update',):
            return fields

        querysets = getattr(self.Meta, 'pk_update_querysets', {})

        for f in [f for f in fields if not getattr(fields[f], 'read_only', True)]:

            new_field = self._get_pk_field(fields[f], querysets.get(f))
            if new_field:
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
    category = CategorySerializer(required=False, help_text='spam', read_only=True)
    # category = CategorySerializer(required=False, help_text='spam')
    tags = TagSerializer(many=True, help_text='tag dayo', required=False)

    # tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())

    class Meta:
        model = Article
        # exclude = ('category',)
        fields = '__all__'

        pk_update_querysets = {
            'tags': Tag.objects.filter(name__startswith='w')
        }
