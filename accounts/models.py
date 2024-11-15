from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone

NULLABLE = {'null': True, 'blank': True}

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Электронная почта должно быть установлено')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=150, default='',unique=True)
    phone_number = models.CharField(max_length=15, default='', **NULLABLE, verbose_name='Номер телефона')
    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=30, **NULLABLE, verbose_name='Имя')
    last_name = models.CharField(max_length=30, **NULLABLE, verbose_name='Фамилия')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Дата регистрации')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_staff = models.BooleanField(default=False, verbose_name='Суперпользователь')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email


