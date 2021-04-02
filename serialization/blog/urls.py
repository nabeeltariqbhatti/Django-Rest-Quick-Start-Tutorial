from django.contrib import admin
from django.urls import path
from .views import POSTList, PostDetail, UserList, UserDetail

urlpatterns = [
    path('', POSTList.as_view(), name='list'),
    path('<pk>/', PostDetail.as_view(), name='post_detail'),
    path('users/', UserList.as_view()),
    path('users/<int:pk>/', UserDetail.as_view()),
]
