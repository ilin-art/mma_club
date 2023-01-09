# # from django.core.mail import send_mail
# # from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# # from django.contrib.auth.models import PermissionsMixin
# # # from django.contrib.auth.validators import UnicodeUsernameValidator
# # from django.db import models
# # # from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# # class UserManager(BaseUserManager):
# #     use_in_migrations = True
# #     def _create_user(self, email, phone_number, first_name, password, **extra_fields):
# #         """
# #         Create and save a user with the given phone_number, email,
# #         first_name, and password.
# #         """
# #         if not email:
# #             raise ValueError('Нужно ввести email')
# #         if not phone_number:
# #             raise ValueError('Нужно ввести номер телефона')
# #         if not first_name:
# #             raise ValueError('TНужно ввести имя')
# #         email = self.normalize_email(email)
# #         user = self.model(
# #             email=email, first_name=first_name, phone_number=phone_number,
# #             **extra_fields
# #         )
# #         user.set_password(password)
# #         user.save(using=self._db)
# #         return user
# #     def create_user(self, email, phone_number, first_name, password=None, **extra_fields):
# #         extra_fields.setdefault('is_staff', False)
# #         extra_fields.setdefault('is_superuser', False)
# #         return self._create_user(
# #             email, phone_number, first_name, password, **extra_fields
# #         )
# #     def create_superuser(self, email, phone_number, first_name, password, **extra_fields):
# #         extra_fields.setdefault('is_staff', True)
# #         extra_fields.setdefault('is_superuser', True)
# #         if extra_fields.get('is_staff') is not True:
# #             raise ValueError('Superuser must have is_staff=True.')
# #         if extra_fields.get('is_superuser') is not True:
# #             raise ValueError('Superuser must have is_superuser=True.')
# #         return self._create_user(
# #             email, phone_number, first_name, password, **extra_fields
# #         )


# class User(AbstractBaseUser, PermissionsMixin):
#     # username_validator = UnicodeUsernameValidator()

#     # username = models.CharField(
#     #     max_length=150,
#     #     unique=True,
#     #     validators=[username_validator],
#     # )
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     middle_name = models.CharField(max_length=255)
#     phoneNumber = PhoneNumberField(unique = True, null = False, blank = False)

#     # username = models.CharField(max_length=150,
#     #                             verbose_name='Логин')
#     # first_name = models.CharField(max_length=150,
#     #                               verbose_name='Имя')
#     # last_name = models.CharField(max_length=150,
#     #                              verbose_name='Фамилия')
#     # email = models.EmailField(unique=True,
#     #                           verbose_name='Почта')

#     USERNAME_FIELD = 'phoneNumber'
#     REQUIRED_FIELDS = ['first_name']

#     objects = UserManager()

#     def __str__(self):
#         return self.email

#     def get_short_name(self):
#         return self.email

#     def get_full_name(self):
#         return self.first_name

#     def email_user(self, subject, message, from_email=None, **kwargs):
#         send_mail(subject, message, from_email, [self.email], **kwargs)


# users/models.py

from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phoneNumber, full_name, password, **extra_fields):
        """
        Create and save a user with the given email,
        full_name, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        if not full_name:
            raise ValueError('The given full name must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, full_name=full_name, phoneNumber=phoneNumber,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phoneNumber, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, phoneNumber, full_name, password, **extra_fields
        )

    def create_superuser(self, email, phoneNumber, full_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(
            email, phoneNumber, full_name, password, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=255, verbose_name='полное имя')
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    phoneNumber = PhoneNumberField(unique = True, null = False, blank = False, verbose_name = 'телефон в формате +7ХХХХХХХХХХ')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name = 'зарегистрирован')

    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['full_name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    CHOICES = (
        ('Male', 'М'),
        ('Female', 'Ж'),
    )
    gender = models.CharField(max_length=20,
        choices = CHOICES,
        null=True,
        blank=True,
        verbose_name='Пол',
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name='Дата рождения'
    )
    height = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Рост'
    )
    weight = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Вес'
    )
    def __str__(self):
        return self.user.full_name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'