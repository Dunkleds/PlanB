from django.urls import path

from .views import me, private_ping, register_user

app_name = "users"

urlpatterns = [
    path("register/", register_user, name="register"),
    path("auth/me/", me, name="me"),
    path("auth/ping/", private_ping, name="private_ping"),
]
