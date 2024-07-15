# yourapp/permissions.py
from rest_framework.permissions import BasePermission
from .models import Company

class IsCompanyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
