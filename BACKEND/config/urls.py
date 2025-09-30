from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from users.views import DispatchInfoViewSet, EmailTokenObtainPairView


def health(_request):
    return JsonResponse({"status": "ok"})


def home(_request):
    return JsonResponse({"message": "Backend online"})


router = DefaultRouter()
router.register(r"api/dispatch", DispatchInfoViewSet, basename="dispatch")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/", include("users.urls")),
    path("api/", include("products.urls")),
    path("", include(router.urls)),
    path("health/", health),
    path("", home),
]
