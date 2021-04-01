from django.contrib import admin
from django.urls import path
from .views import post_list, post_detail

urlpatterns = [
    path('', post_list, name='list'),
    path('<pk>/', post_detail, name='post_detail'),
]
