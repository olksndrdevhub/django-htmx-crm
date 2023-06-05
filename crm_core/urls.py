from django.urls import path

from . import views

app_name = 'crm_core'

urlpatterns = [
    path('', views.home_view, name='home_view'),
    path('products/', views.products_view, name='products_view'),
    path('hx_add_order/', views.hx_add_order, name='hx_add_order'),
    path('hx_add_client/', views.hx_add_client, name='hx_add_client'),
    path('hx_add_product/', views.hx_add_product, name='hx_add_product'),
    path('hx_delete_product/<int:id>/', views.hx_delete_product, name='hx_delete_product'),
]
