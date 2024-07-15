from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Company, Location, Sensor, SensorData, Admin
from .serializers import LocationSerializer, SensorSerializer, SensorDataSerializer, CompanySerializer, AdminSerializer
from .authentication import CompanyAuthentication, SensorAuthentication
from .permissions import IsCompanyAuthenticated
from rest_framework.permissions import AllowAny
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken

class AdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Implementación de tu lógica para la vista de administrador
        return Response({'message': 'Bienvenido, administrador.'})

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'error': 'Debe proporcionar un nombre de usuario y contraseña.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Este nombre de usuario ya está en uso.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return Response({'message': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        login(request, user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Inicio de sesión exitoso.',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        })

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Sesión cerrada exitosamente.'})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.all()


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = [CompanyAuthentication]
    permission_classes = [IsAuthenticated, IsCompanyAuthenticated]

    def get_queryset(self):
        return Location.objects.filter(company_id=self.request.user)

class SensorViewSet(viewsets.ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    authentication_classes = [CompanyAuthentication]
    permission_classes = [IsAuthenticated, IsCompanyAuthenticated]

    def get_queryset(self):
        return Sensor.objects.filter(location_id__company_id=self.request.user)
    
class SensorDataViewSet(viewsets.ModelViewSet):
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer
    authentication_classes = [SensorAuthentication]
    permission_classes = [IsAuthenticated, AllowAny]  # Permitir acceso autenticado y sin autenticar

    def create(self, request, *args, **kwargs):
        api_key = request.headers.get('Sensor-Api-Key')
        if not api_key:
            return Response({'detail': 'Sensor-Api-Key header is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            sensor = Sensor.objects.get(sensor_api_key=api_key)
        except Sensor.DoesNotExist:
            return Response({'detail': 'Invalid API key'}, status=status.HTTP_400_BAD_REQUEST)

        request.data['sensor_id'] = sensor.ID  # Ajusta aquí para usar ID
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def query(self, request):
        from_timestamp = request.query_params.get('from')
        to_timestamp = request.query_params.get('to')
        sensor_ids = request.query_params.getlist('sensor_id')

        # Verifica si los timestamps están presentes y en formato correcto
        if not from_timestamp or not to_timestamp:
            return Response({'detail': 'Required parameters: from, to'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Intenta convertir los timestamps a objetos datetime
            from_timestamp = datetime.fromisoformat(from_timestamp)
            to_timestamp = datetime.fromisoformat(to_timestamp)
        except ValueError:
            return Response({'detail': 'Invalid timestamp format'}, status=status.HTTP_400_BAD_REQUEST)

        # Filtra los datos de SensorData según los parámetros
        queryset = self.get_queryset().filter(
            sensor_id__in=sensor_ids,
            sensor_data_time__gte=from_timestamp,
            sensor_data_time__lte=to_timestamp
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
