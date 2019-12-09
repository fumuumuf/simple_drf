from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^graph', views.GraphModelsView.as_view(), name='graph_models_view'),
    url(r'^table', views.TableView.as_view(), name='db_table_layout_view'),
]
