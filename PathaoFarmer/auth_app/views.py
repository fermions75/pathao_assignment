# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegisterSerializer, LoginSerializer
from farms.repository import FarmsRepository
from livestock.repository import LivestockRepository
from django.db import transaction
from PathaoFarmer.exceptions import CustomAPIException


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    farm_repository = FarmsRepository()
    livestock_repository = LivestockRepository()

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                user = User.objects.get(username=serializer.validated_data['username'])
                farm = self.farm_repository.create_farm(user)
                self.livestock_repository.create_livestock_after_reg(farm)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("serializer.errors: ", serializer.errors)
        raise CustomAPIException(detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                token_serializer = TokenObtainPairSerializer(data=request.data)
                if token_serializer.is_valid():
                    return Response(token_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                if not User.objects.filter(username=username).exists():
                    return Response({'detail': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'detail': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        raise CustomAPIException(detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            print(f"Exception: {e}")
            raise CustomAPIException(detail="Invalid token", code=status.HTTP_400_BAD_REQUEST)