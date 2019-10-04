from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ArticleViewSet, base_name='article')
urlpatterns = router.urls
