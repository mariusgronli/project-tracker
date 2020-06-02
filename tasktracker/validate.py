from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validation(string):
    not_allowed = '[@_!#$%^&*()<>?/\|}{~:]'
    for char in not_allowed:
        if char in string:
            return False

def validate_special_char(value):
    if validation(value) == False:
        raise ValidationError(
            _('Project name contains a special character'),
            params={'value': value},
        )
