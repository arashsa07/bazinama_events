from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.conf import settings


User = get_user_model()
auth_user_settings = getattr(settings, 'AUTH_USER', {})


class SMSBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, username=None, password=None, **kwargs):
        PhoneNumberField = User._meta.get_field('phone_number')
        try:
            phone_number = int(username)
            PhoneNumberField.run_validators(phone_number)
            user = User._default_manager.get_by_phone_number(phone_number)
            if password in user.get_verify_codes():
                return user
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            User().set_password(password)
        except (ValueError, ValidationError) as e:
            print('SMS User Login Error: user -> %s, pass -> %s, detail -> %s' % (username, password, e))
            pass
