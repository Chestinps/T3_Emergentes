from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import AdminSerializer, CompanySerializer, LocationSerializer, SensorSerializer, SensorDataSerializer
from .models import Admin, Company, Location, Sensor, SensorData
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import jwt, datetime

# Create your views here.

class JWTAuthenticationMixin:
    def get_user_from_token(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return None, 'You are not authenticated'

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return None, 'You are not authenticated'

        user = Admin.objects.get(id=payload['id'])
        return user, None

class AdminView(JWTAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user, error = self.get_user_from_token(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

class CompanyView(JWTAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user, error = self.get_user_from_token(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

class LocationView(JWTAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user, error = self.get_user_from_token(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

class SensorView(JWTAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = SensorSerializer
    queryset = Sensor.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user, error = self.get_user_from_token(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

class SensorDataView(JWTAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = SensorDataSerializer
    queryset = SensorData.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user, error = self.get_user_from_token(request)
        if error:
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)
        return super().list(request, *args, **kwargs)

class RegistrationView(APIView):
    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = Admin.objects.filter(username=username, password=password)
        
        if user:
            payload = {
                'id': user[0].id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }

            token = jwt.encode(payload, 'secret', algorithm='HS256')

            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)

            return response
        return Response('Login Failed', status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return Response('You are not authenticated', status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response('You are not authenticated', status=status.HTTP_401_UNAUTHORIZED)

        user = Admin.objects.get(id=payload['id'])
        serializer = AdminSerializer(user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
