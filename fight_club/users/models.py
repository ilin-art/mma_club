from phonenumber_field.modelfields import PhoneNumberField

from django.core.mail import send_mail
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from training_calendar.models import Label


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
    is_trainer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    training_counts = models.ManyToManyField(
        Label,
        related_name='users_have_trains',
        through='TrainingCount',
        verbose_name='Количество тренировок',
    )

    USERNAME_FIELD = 'phoneNumber'
    REQUIRED_FIELDS = ['full_name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def get_email(self):
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
        ('М', 'М'),
        ('Ж', 'Ж'),
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
    photo = models.ImageField(
        null=True,
        blank=True,
        verbose_name='Фото',
        upload_to='profile_photos/'
    )

    def __str__(self):
        return self.user.full_name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class TrainingCount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, verbose_name='Метка')
    count = models.IntegerField(default=0, verbose_name='Количество тренировок')

    def __str__(self):
        return f'{self.user.full_name} - {self.label} ({self.count})'

    class Meta:
        verbose_name = 'Количество тренировок'
        verbose_name_plural = 'Количество тренировок'

# Автоматическое создание профиля и заметки при регистрации
@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    from tasks.models import Task
    if created:
        Profile.objects.create(user=instance)
        Task.objects.create(user=instance)
    else:
        try:
            instance.profile.save()
        except ObjectDoesNotExist:
            Profile.objects.create(user=instance)
            Task.objects.create(user=instance)
