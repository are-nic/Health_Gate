from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from api.permissions import IsAccountOwner


User = get_user_model()


class CurrentUserView(viewsets.ModelViewSet):
    """
    Вывод текущего Пользовтеля
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """
        При запросе выдает текущего пользователя
        """
        return self.request.user

    def list(self, request, *args, **kwargs):
        """
        Переопределение метода и направление его в retrieve для выдачи одного текущего юзера
        """
        return self.retrieve(request, *args, **kwargs)


class UserView(viewsets.ModelViewSet):
    """
    Просмотр, создание, редактирование, удаление аккаунтов.
    get, post, put, patch, delete

    Доступы: Создать аккаунт могут любые пользовтели
            Получить информацию об аккаунтах могу любые авторизованные юзеры
            Изменять, удалять аккаунты могут владельцы аккаунтов и суперпользователь
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Просмотр аккаунтов доступен любому авторизованному пользователю
        Какие-либо дейсвтия над аккаунтами доступны владельцам аккаунтов и суперпользователю
        :return: список разрешений
        """
        if self.request.method == 'POST':
            permission_classes = [AllowAny]
        elif self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAccountOwner]
        return [permission() for permission in permission_classes]

    '''def destroy(self, request, pk=None, **kwargs):
        """
        при удалении аккаунта из группы "bloger" он получает статус Неактивного (is_active = False)
        """
        if request.user.groups.filter(name='bloger').exists():
            request.user.is_active = False
            request.user.save()
            return Response(status=204)'''