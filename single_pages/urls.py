from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('introduction/', views.introduction),
    path('my_page/', views.my_page),
]