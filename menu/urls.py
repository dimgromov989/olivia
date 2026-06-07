from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.MenuListView.as_view(), name='menu-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/<slug:product_slug>/variant/<int:variant_id>/', 
         views.ProductVariantDetailView.as_view(), 
         name='variant-detail'),
]