from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .managers import CustomUserManager
from food.models import Tag


class CustomUser(AbstractUser):
    """Кастомная модель Пользователя"""
    username = None
    phone_number = models.CharField(max_length=12, verbose_name='Номер телефона', unique=True)
    email = models.EmailField(_('email'), blank=True)
    nickname = models.CharField(max_length=50, verbose_name='Никнейм', blank=True)
    full_name = models.CharField(max_length=100, verbose_name='Полное имя', blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес доставки', blank=True)
    about = models.TextField(max_length=300, verbose_name='О Себе', blank=True)
    photo = models.ImageField(verbose_name='Фото профиля', blank=True, null=True, upload_to='profile_photo')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Тэги')
    twitter = models.URLField(verbose_name='Twitter', blank=True)
    facebook = models.URLField(verbose_name='Facebook', blank=True)
    instagram = models.URLField(verbose_name='Instagram', blank=True)
    youtube = models.URLField(verbose_name='Youtube', blank=True)
    tik_tok = models.URLField(verbose_name='Tik-Tok', blank=True)
    patreon = models.URLField(verbose_name='Patreon', blank=True)

    USERNAME_FIELD = 'phone_number'     # сообщает нам, какое поле мы будем использовать для входа
    REQUIRED_FIELDS = []                # запрашиваемые поля при создании суперпользователя

    # Сообщает Django, что класс CustomUserManager должен управлять объектами этого типа.
    objects = CustomUserManager()

    def __str__(self):
        return self.phone_number
