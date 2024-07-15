# yourapp/permissions.py
from rest_framework.permissions import BasePermission
from .models import Company, Sensor

class IsCompanyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Check if request.user is a Company instance
        return isinstance(request.user, Company)
    
class IsSensorAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Check if request.user is a Sensor instance
        return isinstance(request.user, Sensor)
