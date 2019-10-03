from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions
from rest_framework.response import Response

from articles.models import Article
from articles.serializer import ArticleSerializer


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

    permission_classes = [DjangoObjectPermissions,]
    serializer_class = ArticleSerializer
    queryset = Article.objects.prefetch_related('tags')
    filterset_class = ArticleFilterSet
