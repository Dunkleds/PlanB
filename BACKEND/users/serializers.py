from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, trim_whitespace=False)

    class Meta:
        model = User
        fields = ("id", "email", "password", "username", "first_name", "last_name")
        extra_kwargs = {
            "username": {"required": False, "allow_blank": True},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
        }

    def validate_email(self, value: str) -> str:
        value = (value or "").strip().lower()
        if not value:
            raise serializers.ValidationError("El correo es obligatorio.")
        # Unicidad case-insensitive
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Este correo ya está registrado.")
        return value

    def validate_password(self, value: str) -> str:
        # Aplica validadores de Django (si configuraste AUTH_PASSWORD_VALIDATORS)
        validate_password(value)
        return value

    @transaction.atomic
    def create(self, validated_data):
        email = validated_data["email"].strip().lower()
        username = (validated_data.get("username") or email).strip().lower()
        password = validated_data["password"]
        first_name = (validated_data.get("first_name") or "").strip()
        last_name = (validated_data.get("last_name") or "").strip()

        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        return user

class UsernameUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)

    def validate_username(self, value):
        User = get_user_model()
        # Evita colisiones con otros usuarios
        if User.objects.filter(username=value).exclude(pk=self.context["user"].pk).exists():
            raise serializers.ValidationError("Este username ya está en uso.")
        return value


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Permite login con email + password.
    Internamente SimpleJWT usa la clave 'username', así que mapeamos email -> username.
    """

    username_field = "email"

    def validate(self, attrs):
        email = attrs.get("email") or attrs.get("username")
        if not email:
            raise serializers.ValidationError({"email": ["Este campo es requerido."]})
        email = email.strip().lower()
        attrs["username"] = email
        return super().validate(attrs)
