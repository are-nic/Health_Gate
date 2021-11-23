from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from api.permissions import IsAccountOwner


User = get_user_model()


class CurrentUserView(generics.ListAPIView):
    """
    Вывод списка текущего Пользовтеля
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Любой юзер может видеть свой аккаунт и производить над ним действия.
        """
        return User.objects.filter(id=self.request.user.id)


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