from django.conf import settings


User = settings.AUTH_USER_MODEL


class PhoneModelBackend:

    def authenticate(self, phone_number=None, password=None):
        """
        Аутентификация по номеру телефона
        """
        try:
            user = User.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
