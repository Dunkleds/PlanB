import logging
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    DispatchInfoSerializer,
    EmailTokenObtainPairSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
)
from .models import DispatchInfo
from .permissions import IsOwnerOrAdmin

logger = logging.getLogger(__name__)
User = get_user_model()


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


def _collect_errors(error_dict: dict) -> str:
    msgs = []
    for value in error_dict.values():
        if isinstance(value, (list, tuple)):
            msgs.extend(str(v) for v in value)
        elif isinstance(value, dict):
            # Para errores anidados (p.ej., {"password": ["..."]})
            for v in value.values():
                if isinstance(v, (list, tuple)):
                    msgs.extend(str(x) for x in v)
                else:
                    msgs.append(str(v))
        else:
            msgs.append(str(value))
    return " ".join(msgs) or "Error en el registro"

@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])  # evita SessionAuthentication → no exige CSRF en anónimo
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    logger.info("HIT register_user with data=%s", request.data)
    if not serializer.is_valid():
        # Devuelve errores legibles (400), no 500
        return Response(
            {"error": _collect_errors(serializer.errors), "details": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        user = serializer.save()
    except IntegrityError as e:
        logger.warning("IntegrityError en registro: %s", e)
        return Response({"error": "El email/usuario ya existe."}, status=status.HTTP_409_CONFLICT)
    except Exception as e:
        # Loguea y responde limpio (no 500 al cliente)
        logger.exception("Error inesperado en registro: %s", e)
        return Response({"error": "No se pudo crear el usuario."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {
            "message": "Usuario creado",
            "id": user.pk,
            "email": user.email,
            "username": user.get_username(),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me(request):
    user: User = request.user

    if request.method == "GET":
        return Response(
            {
                "id": user.pk,
                "email": user.email,
                "username": user.get_username(),
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )

    serializer = ProfileUpdateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    update_fields = []
    if "first_name" in serializer.validated_data:
        user.first_name = serializer.validated_data["first_name"]
        update_fields.append("first_name")
    if "last_name" in serializer.validated_data:
        user.last_name = serializer.validated_data["last_name"]
        update_fields.append("last_name")

    if update_fields:
        user.save(update_fields=update_fields)

    return Response(
        {
            "message": "Perfil actualizado",
            "id": user.pk,
            "email": user.email,
            "username": user.get_username(),
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        status=status.HTTP_200_OK,
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def private_ping(_request):
    return Response({"message": "pong"})


class DispatchInfoViewSet(viewsets.ModelViewSet):
    serializer_class = DispatchInfoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return DispatchInfo.objects.all()
        return DispatchInfo.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save()
