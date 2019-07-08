from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info

from articles.models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

        # many to many がないならこれでもOK
        # read_only_fields = [f.name for f in Article._meta.fields
        #                     if f.name != 'category']

        _info = get_field_info(Article)
        read_only_fields = [f for f in _info.fields.keys()]
        read_only_fields += [f for f in _info.forward_relations.keys() if f != 'category']
