import uuid
import base64

from django.core.files.base import ContentFile
from django.contrib.auth import get_user_model
from rest_framework import viewsets, decorators, response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer
from api.permissions import IsAccountOwner


User = get_user_model()


class CurrentUserView(viewsets.ModelViewSet):
    """
    Вывод текущего Пользователя
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

    @decorators.action(detail=False, methods=['put'])
    def update_data(self, request):
        photo = None
        if request.data.get('photo'):
            photo = request.data.pop('photo')

        user_query = User.objects.filter(pk=request.user.id)
        user_query.update(**request.data)

        if photo:
            file_format, image_str = photo.split(';base64,')
            ext = file_format.split('/')[-1]
            photo_file = ContentFile(base64.b64decode(image_str), name=f'{uuid.uuid4()}.{ext})')
            user_object = user_query.first()
            user_object.photo = photo_file
            user_object.save()

        return response.Response({"message": "success"})

    @decorators.action(detail=False, methods=['put'])
    def update_password(self, request):
        user = User.objects.get(pk=request.user.id)
        user.set_password(request.data.get('password'))
        user.save()
        return response.Response({"message": "success"})


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
