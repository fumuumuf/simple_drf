from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from articles.models import Article
from articles.serializer import ArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    serializer_class = ArticleSerializer
    queryset = Article.objects.prefetch_related('tags')


    def get_queryset(self):
        print(self.request.get_host())
        return super(ArticleViewSet, self).get_queryset()
