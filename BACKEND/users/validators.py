# users/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class StrongPasswordValidator:
    """
    Requisitos:
    - Longitud mínima (por defecto 10)
    - ≥ 1 mayúscula (A-Z)
    - ≥ 1 minúscula (a-z)
    - ≥ 1 número (0-9)
    - ≥ 1 símbolo (no alfanumérico)
    """
    def __init__(self, min_length=10):
        self.min_length = int(min_length)

    def validate(self, password, user=None):
        errores = []
        if len(password) < self.min_length:
            errores.append(f"• Tener al menos {self.min_length} caracteres.")
        if not re.search(r"[A-Z]", password):
            errores.append("• Incluir al menos una letra MAYÚSCULA (A-Z).")
        if not re.search(r"[a-z]", password):
            errores.append("• Incluir al menos una letra minúscula (a-z).")
        if not re.search(r"\d", password):
            errores.append("• Incluir al menos un número (0-9).")
        if not re.search(r"[^A-Za-z0-9]", password):
            errores.append("• Incluir al menos un símbolo (p. ej., !@#$%).")

        if errores:
            # Mensaje único, claro y en español
            raise ValidationError(
                _("La contraseña no cumple los requisitos:\n") + "\n".join(errores)
            )

    def get_help_text(self):
        return _(
            f"Debe tener ≥ {self.min_length} caracteres e incluir mayúscula, "
            "minúscula, número y símbolo."
        )
