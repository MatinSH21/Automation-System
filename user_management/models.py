from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, User


class EmployeeManager(BaseUserManager):

    def create_user(self, username, email, password, **other_fields):
        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(_("Super user must be assigned to is_staff=True."))

        if other_fields.get('is_superuser') is not True:
            raise ValueError(_("Super user must be assigned to is_superuser=True."))
        return self.create_user(username, email, password, **other_fields)


class Employee(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(_('email'), unique=True)
    date_created = models.DateTimeField(_('created date'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=False)
    is_staff = models.BooleanField(_('is staff'), default=False)
    roles = models.ManyToManyField('Role', symmetrical=False, related_name='employees', blank=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']


class Profile(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('first name'), max_length=30, blank=True)
    gender = models.CharField(_('gender'), max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    address = models.TextField(_('address'), blank=True)
    picture = models.ImageField(_('picture'), upload_to='employee_pictures', default='default.jpg')
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee.username}'s profile"

    class Meta:
        db_table = 'user_management_profile'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Role(models.Model):

    name = models.CharField(_('name'), max_length=50, unique=True)
    permissions = models.ManyToManyField('Permission', symmetrical=False, related_name='roles', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_management_role'
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')


class Permission(models.Model):

    name = models.CharField(_('name'), max_length=50, unique=True)
    codename = models.CharField(_('codename'), max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user_management_permission'
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')
