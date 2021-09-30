from django.contrib.auth.models import BaseUserManager
import phonenumbers


class CustomUserManager(BaseUserManager):
    """
    Определяем модель менеджера для модели Пользователя без поля username
    """

    use_in_migrations = True

    def normalize_phone(self, phone, country_code=None):
        """
        Валидация телефонного номер при регистрации пользователя
        :param phone:
        :param country_code:
        :return: валидный номер телефона
        """
        phone = phone.strip().lower()
        try:
            phone_number = phonenumbers.parse(phone, country_code)
            phone = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        except ImportError:
            pass
        return phone

    def _create_user(self, phone_number, password, **extra_fields):
        """Создает и сохраняет User'a с указанным телефоном и паролем."""
        if not phone_number:
            raise ValueError('Телефонный номер должен быть введен')
        phone_number = self.normalize_phone(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """
        Создает и сохраняет обычного User'a с указанным телефоном и паролем.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """
        Создает и сохраняет SuperUser с указанным телефоном и паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser должен иметь is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)