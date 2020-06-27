import string
import random
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

# Create your models here.
USER_MODEL = settings.AUTH_USER_MODEL


class MyUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.
    Username and password are required. Other fields are optional.
    """

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    avatar = models.ImageField(upload_to='', null=True)

    # aditional fields
    gender = models.BooleanField(choices=(
        (True, "Male"),
        (False, "Female")
    ), default=True)
    about = models.TextField(null=True, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()
    create_adate = models.DateTimeField(auto_now_add=True, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def get_profile_img(self):
        if self.avatar:
            return self.avatar.url
        else:
            return "https://t4.ftcdn.net/jpg/00/64/67/63/240_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"

    def __str__(self):
        return self.email


def generate_token(size=120, chars=string.ascii_letters + string.digits):
    return "".join([random.choice(chars) for _ in range(size)])


class Verification(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=120, default=generate_token)
    verification_type = models.IntegerField(
        choices=(
            (0, "Password"),
            (1, "Email")
        ), default=0
    )
    expire = models.BooleanField(default=False)

    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.token}"

    def get_verify_url(self):
        return reverse("verify_passw", kwargs={"token": self.token,
                                               "user_id": self.user_id})


class News(models.Model):
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    images = models.ImageField(upload_to='')

    create_date = models.DateTimeField(auto_now_add=True)

    def get_image(self):
        if self.images:
            return self.images.url
        else:
            return "https://t4.ftcdn.net/jpg/00/64/67/63/240_F_64676383_LdbmhiNM6Ypzb3FM4PPuFP9rHe7ri8Ju.jpg"

    # def __str__(self):
    #     return self.created_by


class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    create_adate = models.DateTimeField(auto_now_add=True, null=True)


class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    create_adate = models.DateTimeField(auto_now_add=True, null=True)
