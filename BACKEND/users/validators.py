# users/validators.py
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class UpperLowerSymbolValidator:
    """
    Requiere al menos: 1 mayúscula, 1 minúscula y 1 símbolo.
    (No exigimos dígitos porque no lo pediste.)
    """
    def validate(self, password, user=None):
        if not re.search(r"[A-Z]", password):
            raise ValidationError(_("La contraseña debe incluir al menos una letra MAYÚSCULA."))
        if not re.search(r"[a-z]", password):
            raise ValidationError(_("La contraseña debe incluir al menos una letra minúscula."))
        if not re.search(r"[^A-Za-z0-9]", password):
            raise ValidationError(_("La contraseña debe incluir al menos un símbolo (p. ej. !@#$%)."))

    def get_help_text(self):
        return _("Debe contener al menos una mayúscula, una minúscula y un símbolo.")
