from django.urls import path

from .views import django_suspense_loader

urlpatterns = [
    path(
        'suspense/',
        django_suspense_loader,
        name='django_suspense_loader',
    )
]
