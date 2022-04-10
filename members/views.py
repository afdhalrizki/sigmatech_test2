# from django.shortcuts import render
from .models import User
from .serializers import RegisterSerializer, ProfileSerializer, MyTokenObtainPairSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    # permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, format=None):
        
        user = User.objects.get(id=request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        serializer = ProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
