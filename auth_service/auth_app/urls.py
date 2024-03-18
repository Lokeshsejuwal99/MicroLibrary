from django.urls import path
from .views import RegisterViewSet

urlpatterns = [
    path("register/", RegisterViewSet.as_view(), name="register"),
]
