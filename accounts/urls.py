from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = 'accounts'

urlpatterns = [
    path('auth/', views.auth, name='auth'),
    path("logout/", LogoutView.as_view(), name="logout"),

    path('hx_registration/', views.hx_registration, name='hx_registration'),
    path('hx_login/', views.hx_login, name='hx_login'),
]