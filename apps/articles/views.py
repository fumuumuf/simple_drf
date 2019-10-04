from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import FilterSet
from rest_access_policy import AccessPolicy
from rest_framework import viewsets
from rest_framework.response import Response

from articles.models import Article
from articles.serializer import ArticleSerializer


class ArticleAccessPolicy(AccessPolicy):
    statements = [
        # all access is implicitly denied by default
        {
            "action": ["list", "retrieve"],
            "principal": "*",
            "effect": "allow"
        },
        {
            "action": ["publish", "unpublish"],
            "principal": ["group:editor"],
            "effect": "allow"
        },
        # is_author True なら delete 可能
        {
            "action": ["delete"],
            "principal": ["*"],
            "effect": "allow",
            "condition": "is_author"
        },
        # condition が true なら, 全員 deny
        {
            "action": ["*"],
            "principal": ["*"],
            "effect": "deny",
            "condition": "is_happy_hour"
        }
    ]

    def is_author(self, request, view, action) -> bool:
        article = view.get_object()
        return request.user == article.author

    def is_happy_hour(self, request, view, action) -> bool:
        now = datetime.datetime.now()
        return now.hour >= 17 and now.hour <= 18

        @classmethod
        def scope_queryset(cls, request, queryset):
            if request.user.groups.filter(name='editor').exists():
                return queryset

            return queryset.filter(status='published')

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
