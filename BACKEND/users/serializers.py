from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Frontend envía solo email y password
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    # Lo exponemos solo de salida para que el cliente sepa con qué username quedó
    username = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "username")

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
        raw_password = validated_data["password"]

        # Genera username único a partir del local-part del email
        base = email.split("@")[0] or "user"
        username = base
        i = 1
        while User.objects.filter(username=username).exists():
            i += 1
            username = f"{base}{i}"

        # create_user hashea el password y respeta campos del User model
        user = User.objects.create_user(username=username, email=email, password=raw_password)
        return user

class UsernameUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=3, max_length=150)

    def validate_username(self, value):
        User = get_user_model()
        # Evita colisiones con otros usuarios
        if User.objects.filter(username=value).exclude(pk=self.context["user"].pk).exists():
            raise serializers.ValidationError("Este username ya está en uso.")
        return value

