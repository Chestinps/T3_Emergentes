# yourapp/permissions.py
from rest_framework.permissions import BasePermission
from .models import Company

class IsCompanyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Check if request.user is a Company instance
        return isinstance(request.user, Company)
