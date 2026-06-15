from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # 1. VALIDATE
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 2. USER CREATE
        with transaction.atomic():
            user = User.objects.create_user(
                username=data["username"],
                email=data["email"],
                password=data["password"],
            )

            company = user.company
            company.company_name = data["company_name"]
            company.save()

        # 3. JWT
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
            {
                "username": user.username,
                "company_name": company.company_name,
                "api_key": company.api_key,
                "access": access,
            },
            status=status.HTTP_201_CREATED,
        )

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        # 1. VALIDATE
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 2. AUTHENTICATE
        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if user is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 3. JWT
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        company = user.company

        return Response(
            {
                "username": user.username,
                "company_name": company.company_name,
                "api_key": company.api_key,
                "access": access,
            },
            status=status.HTTP_200_OK,
        )
