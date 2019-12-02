from rest_framework.serializers import ModelSerializer
from articles.models import Tag, Category, Article


class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'
