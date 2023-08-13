from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    STATUS_NEW = '0_new'
    STATUS_ACTIVATED = '1_activated'
    STATUS_BANNED = '2_banned'
    STATUS_DELETED = '3_deleted'
    STATUS_CHOICES = [(STATUS_NEW, 'new'), (STATUS_ACTIVATED, 'activated'), (STATUS_BANNED, 'banned'),
                      (STATUS_DELETED, 'deleted')]

    username = None
    objects = UserManager()
    # creation_time - User.date_joined
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEW)
    city = models.CharField(max_length=128, blank=True)
    # family_status = models.CharField(max_length=45, blank=True)  # !!! доделать !!!
    about = models.CharField(max_length=128, blank=True)
    # dark_theme = models.BooleanField(default=False)
    # profile_pic = models.ImageField(upload_to='avatar', default='avatar/default.jpg')  # install Pillow
    friends = models.ManyToManyField('User', related_name='user_friends', blank=True, default=None)
    # groups = models.ManyToManyField('Group', related_name='user_groups', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.id} _ {self.first_name} {self.last_name}'


@receiver(pre_save, sender=User)
def name_uppercase_first_letter(sender, instance, *args, **kwargs):
    instance.first_name = instance.first_name.title()
    instance.last_name = instance.last_name.title()
    instance.city = instance.city.title()
