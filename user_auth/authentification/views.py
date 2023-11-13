from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from .utils import send_email_otc

from .serializers import UserCreateSerializer, UserLoginSerializer


# Create your views here.

class CreateUserView(APIView):
    """
    Представление для регистрации пользователя.
    """
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(status=HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    """
    Представление для входа пользователя.
    """
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=HTTP_200_OK)
        response.set_cookie('access_token', serializer.data.get('access_token'))
        response.set_cookie('refresh_token', serializer.data.get('refresh_token'))

        return response