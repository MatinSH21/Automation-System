from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User
from django.contrib.auth.validators import UnicodeUsernameValidator

from .validators import validate_phone_number, validate_birth_date

from PIL import Image


class EmployeeManager(BaseUserManager):

    def create_user(self, username, password, **other_fields):
        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('role', 'admin')

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Super user must be assigned to is_staff=True."))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Super user must be assigned to is_superuser=True."))
        return self.create_user(username, password, **other_fields)


class Employee(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    ]

    username = models.CharField(_('username'), validators=[UnicodeUsernameValidator()], max_length=30, unique=True)
    date_created = models.DateTimeField(_('created date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=True)
    is_staff = models.BooleanField(_('is staff'), default=False)
    role = models.CharField(_('role'), max_length=15, choices=ROLE_CHOICES)

    objects = EmployeeManager()

    USERNAME_FIELD = 'username'

    def save(self, *args, **kwargs):
        if self.role == "admin":
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True, validators=[validate_birth_date])
    email = models.EmailField(_('email'), unique=True, blank=True, null=True)
    phone_number = models.CharField(
        _('phone number'), max_length=11,
        validators=[validate_phone_number], blank=True)
    address = models.TextField(_('address'), blank=True)
    picture = models.ImageField(_('picture'), upload_to='employee_pictures', default='employee_default_pic.jpg')
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username}'s profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.picture.path)
        if image.height > 300 or image.width > 300:
            output_size = (300, 300)
            image.thumbnail(output_size)
            image.save(self.picture.path)

    class Meta:
        db_table = 'user_management_profile'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
