from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from .models import DispatchInfo

User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    username = serializers.CharField(read_only=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    class Meta:
        model = User
        fields = ("id", "email", "password", "username", "first_name", "last_name")

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
        first_name = (validated_data.get("first_name") or "").strip()
        last_name = (validated_data.get("last_name") or "").strip()

        # Genera username único a partir del local-part del email
        base = email.split("@")[0] or "user"
        username = base
        i = 1
        while User.objects.filter(username=username).exists():
            i += 1
            username = f"{base}{i}"

        # create_user hashea el password y respeta campos del User model
        user = User.objects.create_user(
            username=username,
            email=email,
            password=raw_password,
            first_name=first_name,
            last_name=last_name,
        )
        return user


class ProfileUpdateSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    def validate(self, attrs):
        first_name = attrs.get("first_name")
        last_name = attrs.get("last_name")
        if first_name is None and last_name is None:
            raise serializers.ValidationError({"detail": "Proporciona al menos un campo."})
        if first_name is not None:
            attrs["first_name"] = first_name.strip()
        if last_name is not None:
            attrs["last_name"] = last_name.strip()
        return attrs


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

        password = attrs.get("password")
        if not password:
            raise serializers.ValidationError({"password": ["Este campo es requerido."]})

        email = email.strip().lower()

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            self.fail("no_active_account")
        except User.MultipleObjectsReturned:
            self.fail("no_active_account")

        self.user = authenticate(
            request=self.context.get("request"),
            username=user.get_username(),
            password=password,
        )

        if not self.user:
            self.fail("no_active_account")

        refresh = self.get_token(self.user)

        data = {"refresh": str(refresh), "access": str(refresh.access_token)}

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class DispatchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DispatchInfo
        fields = (
            "id",
            "label",
            "recipient_name",
            "phone",
            "street",
            "number",
            "apartment",
            "commune",
            "city",
            "region",
            "country",
            "postal_code",
            "is_default",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate(self, attrs):
        user = self.context["request"].user
        creating = self.instance is None

        if creating:
            count = DispatchInfo.objects.filter(user=user).count()
            if count >= 2:
                raise serializers.ValidationError(
                    "Solo puedes registrar hasta 2 direcciones de despacho."
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        is_default = validated_data.get("is_default", False)

        obj = DispatchInfo.objects.create(user=user, **validated_data)

        if is_default:
            DispatchInfo.objects.filter(user=user).exclude(pk=obj.pk).update(is_default=False)
        else:
            if DispatchInfo.objects.filter(user=user).count() == 1:
                obj.is_default = True
                obj.save(update_fields=["is_default"])
        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        is_default = validated_data.get("is_default", instance.is_default)
        for field, val in validated_data.items():
            setattr(instance, field, val)
        instance.save()

        if is_default:
            DispatchInfo.objects.filter(user=instance.user).exclude(pk=instance.pk).update(
                is_default=False
            )
        return instance



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8)