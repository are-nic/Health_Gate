from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework import serializers

from food.models import Tag

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['name']


class UserSerializer(serializers.ModelSerializer):
    """
    При регистрации пользователя запрашивается доп поле с указанием группы: 'bloger' или 'customer'
    Можно задать значения имеющихся Тегов
    """
    groups = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Group.objects.all(),
                                          required=True,
                                          allow_null=False,
                                          allow_empty=False)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())

    def create(self, validated_data):
        """
        Хеширование поступающего пароля при регистрации через POST-запрос
        Установка значения поля is_active = True.
        """
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['is_active'] = True
        return super(UserSerializer, self).create(validated_data)

    class Meta:
        model = User
        fields = '__all__'
