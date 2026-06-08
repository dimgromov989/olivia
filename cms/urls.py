from cms.apps import CmsConfig
from django.urls import path
from . import views

app_name = CmsConfig.name

urlpatterns = [
    path('blocks/', views.PageBlockListView.as_view(), name='block-list'),
]