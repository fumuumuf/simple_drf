from django.urls import path

from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('ffm', views.FFMViewSet, base_name='ffm')
router.register('', views.ArticleViewSet, base_name='articles')
urlpatterns = router.urls
