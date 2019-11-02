from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.response import Response

from articles.models import Article, FertileForestNode
from articles.serializer import ArticleSerializer, FertileForestNodeSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    class ArticleFilterSet(FilterSet):
        class Meta:
            model = Article
            fields = {
                'id': ['exact']
            }

    serializer_class = ArticleSerializer
    queryset = Article.objects.prefetch_related('tags')
    filterset_class = ArticleFilterSet


class FFMViewSet(viewsets.ModelViewSet):
    serializer_class = FertileForestNodeSerializer
    queryset = FertileForestNode.objects.all()
    def get_queryset(self):
        return super(FFMViewSet, self).get_queryset()
    #
    def get_serializer(self, *args, **kwargs):
        return super(FFMViewSet, self).get_serializer(*args,**kwargs)

