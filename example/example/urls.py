from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('posts.urls')),
    path('_suspense/', include('suspense.urls')),
    path('admin/', admin.site.urls),
]
