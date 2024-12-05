from django.urls import path

from .views import AsyncPostTemplateView, PostTemplateView, async_posts, post, posts

urlpatterns = [
    path('', posts),
    path('class-view/', PostTemplateView.as_view()),
    path('async/', async_posts),
    path('async/class-view/', AsyncPostTemplateView.as_view()),
    path('<str:slug>/', post),
]
