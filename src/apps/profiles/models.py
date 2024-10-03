from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Собственный менеджер для модели пользователя.

    Данный менеджер убирает в отличие от обычного менеджера,
    убирает username при создании пользователя (делает его необязательным).
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Создает и сохраняет пользователя с заданными email и password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Собственная модель пользователя.

    :attr USERNAME_FIELD: Имя поля в модели пользователя, которое используется
                          в качестве уникального идентификатора.
    :attr REQUIRED_FIELDS: Список имен полей, которые будут запрашиваться при
                           создании пользователя с помощью команды управления createsuperuser.
    """

    GENDERS = (
        ('male', 'мужчина'),
        ('female', 'женщина'),
    )

    middle_name = models.CharField(
        _('Отчество'),
        max_length=150,
        null=True, blank=True,
    )
    email = models.EmailField(
        _("Адрес электронной почты"),
        unique=True,
    )
    phone = models.CharField(
        _('Номер телефона'),
        max_length=14,
        unique=True,
        null=True, blank=True,
    )
    avatar = models.ImageField(
        _('Аватар'),
        upload_to='profiles/avatars/',
        null=True, blank=True,
    )
    gender = models.CharField(
        _('Пол'),
        max_length=6,
        choices=GENDERS,
        default='male',
    )
    birthday = models.DateField(
        _('Дата рождения'),
        null=True, blank=True,
    )
    address = models.CharField(
        _('Адрес проживания'),
        max_length=1024,
        null=True, blank=True,
    )
    username = None

    objects = CustomUserManager()

    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.email






