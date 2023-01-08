from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime

from .serializers import UserSerializer
from .models import User


LOGIN_TIMEOUT = 60 #minutes
SECRET = 'secretword'

# Create your views here.
class UserSignup(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserLogin(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email = email)

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Password does not match")

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=LOGIN_TIMEOUT),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, SECRET, algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.get(id = payload['id'])

        serializer = UserSerializer(user)

        return Response(serializer.data)

class UserLogout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }

        return response