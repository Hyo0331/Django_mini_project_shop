from django.urls import path
from . import views

urlpatterns = [
    path('', views.YarnList.as_view()),
    path('update_yarn/<int:pk>/', views.YarnUpdate.as_view()),
    path('<int:pk>/', views.YarnDetail.as_view()),
    path('create_yarn/', views.YarnCreate.as_view()),
    path('tag/<str:slug>/', views.tag_page),
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>/new_comment/', views.new_comment),
    path('search/<str:q>/', views.YarnSearch.as_view()),
]