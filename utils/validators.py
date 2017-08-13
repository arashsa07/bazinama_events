from django.core.validators import RegexValidator
from django.utils.translation import ugettext as _


class PhoneNumberValidator(RegexValidator):
    regex = '^989[0-3,9]\d{8}$'
    message = _('Phone number must be a VALID 12 digits like 989xxxxxxxxx')
    code = 'invalid'


class UsernameValidator(RegexValidator):
    regex = '^[a-zA-Z][a-zA-Z0-9_\.]+$'
    message = 'Enter a valid username starting with a-z. ' \
              'This value may contain only letters, numbers and underscore characters.'
    code = 'invalid'


validate_phone_number = PhoneNumberValidator()
validate_username = UsernameValidator()
