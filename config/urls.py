from django.urls import include, path

urlpatterns = [
    path('/suspense/', include('suspense.urls')),
]
