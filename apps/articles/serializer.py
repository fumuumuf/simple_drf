from rest_framework import serializers

from articles.models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self,*args,**kwargs):
        super(CategorySerializer, self).__init__(*args,**kwargs)
        print(self.context)

    class Meta:
        model = Category
        fields = '__all__'



class ArticleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Article
        fields = '__all__'
