# config/urls.py
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from users.views import register_user, private_ping
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

def health(_): return JsonResponse({'status':'ok'})
def home(_):   return JsonResponse({'message':'Backend online'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_user),
    path('privado/', private_ping),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
    path('health/', health),
    path('', home),
]



from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from users.views import register_user

def health(_): return JsonResponse({'status':'ok'})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', register_user),  # <- AQUÍ creas el endpoint real
    path('health/', health),
]