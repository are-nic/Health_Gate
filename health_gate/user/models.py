from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
    """Кастомная модель Пользователя"""
    phone_number = models.CharField(max_length=11, verbose_name='Номер телефона', unique=True)
    email = models.EmailField(_('email'), unique=True, blank=True)
    full_name = models.CharField(max_length=250, verbose_name='Полное имя', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True)
    about = models.TextField(max_length=300, verbose_name='О Себе', blank=True)
    photo = models.ImageField(verbose_name='Фото профиля', blank=True, null=True, upload_to='profile_photo')

    is_active = models.BooleanField(default=False, verbose_name='Прошел модерацию')

    USERNAME_FIELD = 'phone_number'     # USERNAME_FIELD and password будут запрошены по умолчанию
    REQUIRED_FIELDS = []                # ['full_name'] python manage.py createsuperuser