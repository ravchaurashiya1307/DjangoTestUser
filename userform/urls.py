from django.urls import path
from . import views


urlpatterns = [
    path('user-form/', views.User),
    path('', views.login),
]
