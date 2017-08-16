import random

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, send_mail

from utils.validators import validate_phone_number, validate_username


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, phone_number, email, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number,
                          username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, phone_number=None, email=None, password=None, **extra_fields):
        if username is None:
            if email:
                username = email.split('@', 1)[0]
            if phone_number:
                username = random.choice('abcdefghijklmnopqrstuvwxyz') + str(phone_number)[-7:]
            while User.objects.filter(username=username).exists():
                username += str(random.randint(10, 99))

        return self._create_user(username, phone_number, email, password, False, False, **extra_fields)

    def create_superuser(self, username, phone_number, email, password, **extra_fields):
        return self._create_user(username, phone_number, email, password, True, True, **extra_fields)

    def get_by_phone_number(self, phone_number):
        return self.get(**{'phone_number': phone_number})


class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=32, unique=True,
        help_text=_('Required. 30 characters or fewer starting with a letter. Letters, digits and underscore only.'),
        validators=[validate_username, ],
        error_messages={
            'unique': _("A user with that username already exists."),
        }
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone_number = models.BigIntegerField(_('mobile number'), unique=True, null=True, blank=True,
        validators=[validate_phone_number, ],
        error_messages={
            'unique': _("A user with this mobile number already exists."),
        }
    )
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    verify_codes = models.CharField(_('verification codes'), max_length=30, blank=True,
                                    validators=[validate_comma_separated_integer_list, ])

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    class Meta:
        db_table = 'auth_users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def is_loggedin_user(self):
        """
        Returns True if user has actually logged in with valid credentials.
        """
        return self.phone_number is not None or self.email is not None

    def get_verify_codes(self):
        """
        Return verification codes.
        """
        if self.verify_codes:
            return self.verify_codes.split(',')
        else:
            return []

    def set_verify_code(self, verify_code):
        """
        Sets verification code for user. (Just last five codes saved.)
        """
        vlist = self.get_verify_codes()
        vlist.append(str(verify_code))
        self.verify_codes = ','.join(vlist[-5:])

    def save(self, *args, **kwargs):
        if self.email is not None and self.email.strip() == '':
            self.email = None
        super().save(*args, **kwargs)

    @property
    def has_profile(self):
        return hasattr(self, 'userprofile')


class State(models.Model):
    state_name = models.CharField(_('state name'), max_length=100)

    class Meta:
        db_table = 'locations_states'
        ordering = ('state_name', )
        verbose_name = _('state')
        verbose_name_plural = _('states')

    def __str__(self):
        return self.state_name


class City(models.Model):
    state = models.ForeignKey(State, verbose_name=_('state'))
    city_name = models.CharField(_('city name'), max_length=150)

    class Meta:
        db_table = 'locations_cities'
        ordering = ('city_name', )
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    def __str__(self):
        return '%s - %s' % (self.state, self.city_name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField(_('nick_name'), max_length=150, blank=True)
    avatar = models.ImageField(_('avatar'), blank=True, upload_to='profile_avatars/')
    birthday = models.DateField(_('birthday'))
    gender = models.BooleanField(_('gender'), help_text=_('female is False, male is True'))
    cup_numbers = models.PositiveIntegerField(_('cup numbers'))
    level = models.PositiveSmallIntegerField(_('level'))
    city = models.ForeignKey(City, related_name='city')
    clash_id = models.CharField(_('clash id'), max_length=256)
    email = models.EmailField(_('email address'), blank=True)

    class Meta:
        db_table = 'auth_profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    @property
    def get_first_name(self):
        """
        Returns first name of user.
        """
        return self.user.first_name

    @property
    def get_last_name(self):
        """
        Return last name of user.
        """
        return self.user.last_name
