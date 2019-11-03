from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.response import Response

from articles.models import Article,  Comment
from articles.serializer import ArticleSerializer,  CommentSerializer


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
    queryset = Article.objects.prefetch_related('tags').prefetch_related('comments')
    filterset_class = ArticleFilterSet


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
