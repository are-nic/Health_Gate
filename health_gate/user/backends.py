from django.contrib.auth import get_user_model


User = get_user_model()


class PhoneModelBackend:

    def authenticate(self, phone_number=None, password=None):
        """
        Аутентификация по номеру телефона
        :param phone_number:
        :param password:
        :return:
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
