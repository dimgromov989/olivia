from django.urls import path

from menu.apps import MenuConfig

from . import views

app_name = MenuConfig.name

urlpatterns = [
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path("", views.MenuListView.as_view(), name="menu-list"),
    path(
        "products/<slug:slug>/",
        views.ProductDetailView.as_view(),
        name="product-detail",
    ),
]
