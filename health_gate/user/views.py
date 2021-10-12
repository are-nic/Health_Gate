from django.contrib.auth import get_user_model
from rest_framework import viewsets
from .serializers import UserSerializer


User = get_user_model()


class UserView(viewsets.ModelViewSet):
    """
    Просмотр, создание, редактирование, удаление аккаунтов.
    get, post, put, patch, delete
    Неаутентифицированные пользователи могут отправить GET-запрос для получения списка пользователей,
    но он будет пустым, потому что возвращаемый User.objects.filter (id = self.request.user.id) гарантирует,
    что будет возвращена только информация об аутентифицированном пользователе.

    То же самое относится и к другим методам: если аутентифицированный пользователь пытается УДАЛИТЬ
    другой пользовательский объект, будет возвращено: "Не найдено" (поскольку пользователь, к которому он пытается
    получить доступ, отсутствует в наборе запросов).

    Прошедшие проверку пользователи могут совершать действия над своими аккаунтами.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Если пользователь - Суперпользователь, то он может читать и совершать действия над аккаунтами.
        Любой другой юзер может видеть свой аккаунт и производить над ним действия.
        """
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)

    '''def destroy(self, request, pk=None, **kwargs):
        """
        при удалении аккаунта из группы "bloger" он получает статус Неактивного (is_active = False)
        """
        if request.user.groups.filter(name='bloger').exists():
            request.user.is_active = False
            request.user.save()
            return Response(status=204)'''