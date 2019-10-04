from rest_access_policy import AccessPolicy
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from articles.models import Article
from articles.serializer import ArticleSerializer


class ArticleAccessPolicy(AccessPolicy):
    """
    記事に関するアクセスポリシー

    Note:
        デフォルトはすべてのアクセスを拒否
    """

    statements = [
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
        # is_author True なら delete(action:destroy) 可能
        {
            "action": ["destroy"],
            "principal": ["*"],
            "effect": "allow",
            "condition": "is_author"
        },
    ]

    def is_author(self, request, view, action) -> bool:
        """
        request.user が author であるか？
        """
        # scope_queryset を使用している場合, scope_querysetでのフィルタリングもされることに注意
        article = view.get_object()
        return request.user == article.author

    @classmethod
    def scope_queryset(cls, request, queryset):
        if request.user.groups.filter(name='editor').exists():
            return queryset

        return queryset.filter(status='publish')


class ArticleViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    permission_classes = (ArticleAccessPolicy,)

    @property
    def access_policy(self):
        return self.permission_classes[0]

    serializer_class = ArticleSerializer
    queryset = Article.objects.select_related('category').prefetch_related('tags')

    def get_queryset(self):
        return self.access_policy.scope_queryset(
            self.request, Article.objects.all()
        )

    @action(methods=["POST"], detail=False)
    def publish(self, request, *args, **kwargs):
        return Response('to publish!')

    @action(methods=["POST"], detail=False)
    def unpublish(self, request, *args, **kwargs):
        return Response('to unpublish!')
