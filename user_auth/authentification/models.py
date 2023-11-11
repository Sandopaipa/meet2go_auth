from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    """
    Класс, переопределяющий создание пользователей.
    """
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
        return self.create_user(email, password, first_name, last_name, birthdate, **extra_fields)

class User(AbstractUser):
    username = models.EmailField('email пользователя', primary_key=True)
    first_name = models.CharField('Имя пользователя', max_length=50, blank=False)
    last_name = models.CharField('Фамилия пользователя', max_length=50, blank=False)
    birthdate = models.DateField('День рождения пользователя', blank=False)
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'birthdate'
    ]
    objects = UserManager

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)