from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

from phonenumber_field.modelfields import PhoneNumberField
from imagekit.models import ProcessedImageField
from imagekit.processors import SmartResize, Transpose

# Create your models here.
class CustomMoonUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CrmUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    phone = PhoneNumberField(blank=True, region='UA')
    is_client = models.BooleanField(default=None, blank=True, null=True)
    userpic = ProcessedImageField(
        upload_to='userpics/', blank=True, default='userpics/userpic.jpg',
        processors=[Transpose(), SmartResize(480, 480)], format='JPEG',
        options={'quality': 70})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomMoonUserManager()

    class Meta:
        pass
        ordering = ['-date_joined']

    @property
    def get_crm_url(self):
        return reverse('dashboard:user_profile_view', kwargs={'id': self.id})

    @property
    def get_user_orders(self):
        return self.orders.all()

    @property
    def phone_string(self):
        return str(self.phone)

    @property
    def get_active_orders(self):
        return self.orders.filter(active=True)

    @property
    def have_active_orders(self):
        if self.orders.filter(active=True).count() > 0:
            return True
        return False

    @property
    def have_orders(self):
        if self.orders.all().count() > 0:
            return True
        return False

    @property
    def get_uncompleted_tasks(self):
        return self.tasks.filter(completed=False).count()

    def __str__(self):
        return self.email
