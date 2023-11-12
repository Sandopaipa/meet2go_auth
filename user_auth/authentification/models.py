from django.core.validators import validate_email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.contrib.auth.base_user import BaseUserManager

from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class UserManager(BaseUserManager):
    """
    Класс, переопределяющий создание пользователей для создания пользозвателя по email.
    """

    def _email_validator(self, email):
        try:
            validate_email(email)
        except:
            raise ValueError("Некорректный email. Пожалуйста введите корректный email.")

    def create_user(self, email, password, first_name, last_name, birthdate, **extra_fields):

        if email is None:
            raise ValueError('Введите ваш e-mail')
        if password is None:
            raise ValueError('Введите ваш пароль')
        if first_name is None:
            raise ValueError('Введите ваше имя')
        if last_name is None:
            raise ValueError('Введите вашу фамилию')
        if birthdate is None:
            raise ValueError('Введите вашу дату рождения')

        email = self.normalize_email(email)
        self._email_validator(email)
        user = self.model(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birthdate=birthdate,
            **extra_fields
        )
        user.set_password(password)

        user.save()
        return user
    def create_superuser(self, email, password, first_name, last_name, birthdate, **extra_fields):

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_superuser') is True:
            raise ValueError('Пользователь должен быть суперпользователем')
        if extra_fields.get('staff') is True:
            raise ValueError('Пользователь должен быть сотрудником')
        if extra_fields.get('is_active') is True:
            raise ValueError('Учетная запись пользователя не должна быть отключенной')
        if extra_fields.get('is_verified') is True:
            raise ValueError('Пользователь должен быть верифицирвоан.')

        return self.create_user(email, password, first_name, last_name, birthdate, **extra_fields)

class User(AbstractUser, PermissionsMixin):
    """
    Модель пользователя.
    """
    username = None  # Переопределение поля username. Так как в AbstractUser оно необходимо.

    email = models.EmailField('email пользователя', unique=True)
    first_name = models.CharField('Имя пользователя', max_length=50, blank=False)
    last_name = models.CharField('Фамилия пользователя', max_length=50, blank=False)
    birthdate = models.DateField('День рождения пользователя', blank=False)  # Для персонализации контента на основании возраста

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'birthdate'
    ]
    objects = UserManager()

    def __str__(self):
        return '%s %s | %s' % (self.first_name, self.last_name, self.email)

    @property
    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class OneTimeCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user}: code{self.code}"