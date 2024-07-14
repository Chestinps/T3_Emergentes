# yourapp/authentication.py
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Company

class CompanyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Company-Api-Key')
        if not api_key:
            raise AuthenticationFailed('Company-Api-Key header is required')
        
        try:
            company = Company.objects.get(company_api_key=api_key)
        except Company.DoesNotExist:
            raise AuthenticationFailed('Invalid API key')

        return (company, None)
