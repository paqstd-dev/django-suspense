from django.urls import path

from .views import post, posts

urlpatterns = [path('', posts), path('<str:slug>/', post)]
