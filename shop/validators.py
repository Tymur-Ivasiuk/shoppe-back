from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def starValid(value):
    if not 0 <= value <= 5:
        raise ValidationError(_('%(value) is not in [0; 5]'), params={'value': value})

def validate_positive(value):
    if value < 0:
        raise ValidationError(_('%(value) is not positive'), params={'value': value})

def sale_validate(value):
    if value > 100:
        raise ValidationError(_('%(value) cannot be more than 100'), params={'value': value})
