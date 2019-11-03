from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('comments', views.CommentViewSet, base_name='comments')
router.register('', views.ArticleViewSet, base_name='articles')
urlpatterns = router.urls
