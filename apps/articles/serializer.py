from drf_writable_nested import NestedUpdateMixin, NestedCreateMixin
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info

from articles.models import Article, Category, NeoTagRel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NeoTagRelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NeoTagRel
        # article は 自動的にセットされるので, read_only or exclude で更新対象からはずす
        read_only_fields = ['article']
        fields = '__all__'


class ArticleSerializer(NestedCreateMixin, NestedUpdateMixin, serializers.ModelSerializer):
    # many-to-many で through を挟む項目
    neo_tag_set = NeoTagRelSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = '__all__'
