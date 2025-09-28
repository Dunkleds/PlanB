import logging
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings



from .serializers import (
    DispatchInfoSerializer,
    EmailTokenObtainPairSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer
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




class PasswordResetRequest(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = PasswordResetRequestSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        email = ser.validated_data["email"]

        # Siempre respondemos 200 para no filtrar existencia del usuario
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"ok": True}, status=status.HTTP_200_OK)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:5173")
        reset_link = f"{frontend_url}/reset-password?uid={uid}&token={token}"

        subject = "Restablecer contraseña"
        message = f"Hola,\n\nPara restablecer tu contraseña haz clic aquí:\n{reset_link}\n\nSi no lo solicitaste, ignora este mensaje."
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

        # En dev puedes usar backend de consola. En prod, SMTP (SendGrid/Mailgun/Resend, etc.)
        send_mail(subject, message, from_email, [email], fail_silently=not settings.DEBUG)

        # (opcional en DEBUG) devolver el link para probar rápido
        payload = {"ok": True}
        if settings.DEBUG:
            payload["debug_reset_link"] = reset_link
        return Response(payload, status=status.HTTP_200_OK)


class PasswordResetConfirm(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        ser = PasswordResetConfirmSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        uid = ser.validated_data["uid"]
        token = ser.validated_data["token"]
        new_password = ser.validated_data["new_password"]

        try:
            uid_int = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_int)
        except Exception:
            return Response({"detail": "Enlace inválido."}, status=status.HTTP_400_BAD_REQUEST)

        if not token_generator.check_token(user, token):
            return Response({"detail": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"ok": True, "message": "Contraseña actualizada."}, status=status.HTTP_200_OK)