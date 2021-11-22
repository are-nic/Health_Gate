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
    Создавать рецепты разрешено пользователям из группы "bloger"
    Действия над рецептами доступны владельцам рецептов или суперпользователю
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.owner == request.user and request.user.groups.filter(name='bloger').exists():
            return True
        return False


class IsOwnerRecipeIngredients(permissions.BasePermission):
    """
    Разрешения для добавления ингредиентов к рецептам, владельцем которых является текущий Пользователь
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.recipe.owner == request.user


class IsSuperUser(permissions.BasePermission):
    """
    Кастомное разрешение для Суперпользователя
    """

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class IsAccountOwner(permissions.BasePermission):
    """
    Кастомное разрешение для действий над аккаунтами
    Чтение аккаунтов доступно любому авторизованному юзеру
    Действия над аккаунтами доступны владельцам аккаунтов и суперпользователю
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or obj.id == request.user.id:
            return True
        return False