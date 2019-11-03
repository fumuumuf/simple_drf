import copy
from collections import defaultdict

from django.db import models
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ListSerializer

from articles.models import Article, Category, FertileForestNode, Comment


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(CategorySerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = Category
        fields = '__all__'


class FFMListSerializer(ListSerializer):
    def _representation_forest(self, data):
        if not data:
            return []

        data = sorted(data, key=lambda x: x.queue)
        depth_node = dict()

        root_depth = data[0].depth
        root_nodes = []
        for node in data:
            node.children = []
            if root_depth == node.depth:
                root_nodes.append(node)

            depth_node[node.depth] = node
            if root_depth != node.depth:
                print('add :', depth_node[node.depth - 1], node)
                depth_node[node.depth - 1].children.append(node)

        return root_nodes

    def to_representation(self, data):
        iterable = data.all() if isinstance(data, models.Manager) else data
        root_nodes = self._representation_forest(iterable)
        print(root_nodes)
        return [
            self.child.to_representation(item) for item in root_nodes
        ]

    def update(self, instance, validated_data):
        return super(FFMListSerializer, self).update(instance, validated_data)


class FertileForestNodeSerializer(serializers.ModelSerializer):
    parent = PrimaryKeyRelatedField(queryset=FertileForestNode, required=False, allow_null=True)

    def to_representation(self, instance):
        if getattr(instance, 'children', None):
            # TODO: この child の指定の仕方で正しい？
            self.fields['children'] = ListSerializer(child=self.__class__())
        return super(FertileForestNodeSerializer, self).to_representation(instance)

    # class Meta:
    #     model = FertileForestNode
    #     exclude = ['queue', 'id']
    #     list_serializer_class = FFMListSerializer


class CommentSerializer(FertileForestNodeSerializer):
    parent = PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False, allow_null=True, write_only=True)

    class Meta:
        model = Comment
        exclude = ['queue', ]
        list_serializer_class = FFMListSerializer


class ArticleSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = '__all__'
