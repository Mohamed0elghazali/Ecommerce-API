from django.urls import path

from . import views

urlpatterns = [
    path('products/', views.get_all_products, name='products'),
    path('products/<str:pk>/', views.get_product, name='get_by_id'),
    path('products_byfilter/', views.get_by_filter, name='get_by_filter'),
    path('products_bypage/', views.get_by_page, name='get_by_page'),
    path('products/new', views.new_product, name='new_product'),
    path('products/update/<str:pk>', views.update_product, name='update_product'),
    path('products/delete/<str:pk>', views.delete_product, name='delete_product'),
]