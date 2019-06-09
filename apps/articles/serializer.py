from rest_framework import serializers
from rest_framework.serializers import Serializer
import copy

from articles.models import Article, Category


class PKWritableMixin:

    def __init__(self, *args, **kwargs):
        self.org_pk_fields = {}
        super(PKWritableMixin, self).__init__(*args, **kwargs)

    def exchange_pk_field(self, f):
        field = self._declared_fields[f]
        if getattr(field, 'read_only', True):
            return

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
        self.org_pk_fields[f] = field
        self._declared_fields[f] = new_field

    def get_fields(self):

        if getattr(self.context.get('view'), 'action', '') not in ('create', 'update', 'partial_update',):
            return super(PKWritableMixin, self).get_fields()

        # ModelSerializer の get_fields を呼び出す前に 定義されている ModelSeiralizer のフィールドを PrimaryKeyRelatedField に付け替えておく.
        # これは ModelSerializer にて Meta の設定, _declared_fields やモデルの情報などを組み合わせて _fields を組み立てているので
        # 念の為このような実装にした.(気にしすぎかもしれないが...)

        # org_declared_fields = copy.deepcopy(self._declared_fields)
        # print('1:',org_declared_fields)
        # for f in [f for f in self._declared_fields if
        #           isinstance(self._declared_fields[f], serializers.ModelSerializer)]:
        #     self.exchange_pk_field(f)

        res = super(PKWritableMixin, self).get_fields()
        # self._declared_fields = org_declared_fields
        print('2:',self._declared_fields)
        print('fields: ',res['category'])
        return res

    def to_representation(self, obj):
        res = super(PKWritableMixin, self).to_representation(obj)
        for f, _serializer in self.org_pk_fields.items():
            source = getattr(self.fields[f], 'source') or f
            print(f, source)
            if f in res:
                print(_serializer.to_representation(getattr(obj, source)))
                res[f] = _serializer.to_representation(getattr(obj, source))
        return res

    class Meta:
        model = Article
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(PKWritableMixin, serializers.ModelSerializer):
    category = CategorySerializer(required=False, help_text='spam')
    # alter_category = CategorySerializer(required=False, help_text='spam', source='category')

    class Meta:
        model = Article
        # exclude = ('category',)
        fields = '__all__'
