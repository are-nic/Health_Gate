"""Модуль кастомных разрешений"""
from rest_framework import permissions


class CustomerOrderOrReadOnly(permissions.BasePermission):
    """
    Кастомное разрешение только для создателей заказа или Админа (is_staff)
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if obj.customer == request.user or request.user.is_staff:
            return True
        return False