"""Модуль кастомных разрешений"""
from rest_framework import permissions


class CustomerOrderOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение только для создателей заказа или Суперпользователя
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.customer == request.user or request.user.is_superuser:
            return True
        return False


class AuthorComment(permissions.BasePermission):
    """
    Кастомное разрешение для действий над комментариями
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.author == request.user or request.user.is_superuser:
            return True
        return False


class RecipeOwner(permissions.BasePermission):
    """
    Кастомное разрешение для действий над рецептами
    Чтение рецептов доступно любому авторизованному пользователю.
    Действия над рецептами доступны владельцам рецептов, входящих в группу "bloger" или суперпользователю
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user and request.user.groups.filter(name='bloger').exists():
            return True
        elif request.user.is_superuser:
            return True
        return False