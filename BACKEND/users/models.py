from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass


class DispatchInfo(models.Model):
    """Dirección de despacho asociada a un usuario."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dispatch_infos",
        db_index=True,
    )
    label = models.CharField(max_length=40, default="Principal")
    recipient_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30, blank=True)
    street = models.CharField(max_length=120)
    number = models.CharField(max_length=20, blank=True)
    apartment = models.CharField(max_length=20, blank=True)
    commune = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80)
    region = models.CharField(max_length=80, blank=True)
    country = models.CharField(max_length=60, default="Chile")
    postal_code = models.CharField(max_length=20, blank=True)

    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "despacho_info"
        ordering = ["-is_default", "-updated_at", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "label"], name="uniq_dispatch_label_per_user"
            ),
        ]

    def __str__(self):
        return f"{self.user_id} · {self.label} · {self.city}"
