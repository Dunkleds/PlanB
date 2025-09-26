from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import RegisterSerializer

User = get_user_model()


def _collect_errors(error_dict: dict) -> str:
    messages: list[str] = []
    for value in error_dict.values():
        if isinstance(value, (list, tuple)):
            messages.extend(str(item) for item in value)
        else:
            messages.append(str(value))
    return " ".join(messages) or "Error en el registro"


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        try:
            serializer.save()
        except IntegrityError:
            return Response({"error": "El email/usuario ya existe"}, status=status.HTTP_409_CONFLICT)
        return Response({"message": "Usuario creado"}, status=status.HTTP_201_CREATED)

    error_msg = _collect_errors(serializer.errors)
    return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user: User = request.user
    return Response(
        {
            "id": user.pk,
            "email": user.email,
            "username": user.get_username(),
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def private_ping(_request):
    return Response({"message": "pong"})
