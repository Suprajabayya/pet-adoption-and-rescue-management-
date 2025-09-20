from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer, PetSerializer
from .models import Pet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User


# ---------------- REGISTER ----------------
class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            if User.objects.filter(username=email).exists():
                return Response({'detail': 'User with this email already exists.'}, status=400)
            try:
                user = serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user': UserSerializer(user).data}, status=201)
            except IntegrityError:
                return Response({'detail': 'User with this email already exists.'}, status=400)
        return Response(serializer.errors, status=400)


# ---------------- LOGIN ----------------
class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password required.'}, status=400)

        # Authenticate using username=email
        user = authenticate(username=email, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data}, status=200)
        return Response({'detail': 'Invalid credentials'}, status=400)


# ---------------- PET LIST / CREATE ----------------
class PetListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PetSerializer
    queryset = Pet.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(reported_by=self.request.user)
