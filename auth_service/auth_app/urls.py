from django.urls import path
from .views import RegisterViewSet, LoginViewSet

urlpatterns = [
    path("register/", RegisterViewSet.as_view(), name="register"),
    path("login/", LoginViewSet.as_view(), name="login"),
]
