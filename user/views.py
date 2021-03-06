import json
import bcrypt
import jwt

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from my_settings import SECRET_KEY,ALGORITHM
from user.models import User
from user.utils import login_decorator


class SignInView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_name', 'password'],
            properties={
                'user_name': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='sign in with existing username and password'
    )
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            user_name   = data['user_name']
            password    = data['password']
            
            if not User.objects.filter(user_name=user_name).exists():
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)
            
            user = User.objects.get(user_name=user_name)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

                return JsonResponse({'MESSAGE':'SUCCESS', "access_token" : access_token}, status=200)
            return JsonResponse({'MESSAGE':'SIGNIN_FAIL'}, status=401)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALID_KEYS'}, status=400)

PASSWORD_MIN_LENGTH     = 6
USER_NAME_MIN_LENGTH    = 3
USER_NAME_MAX_LENGTH    = 32

class UserView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['user_name', 'password', 'nickname', 'email'],
            properties={
                'user_name': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'nickname': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
            },
        ),
        operation_description='sign up to make a new account'
    )
    def post(self, request):
        data = json.loads(request.body)
        
        try:
            user_name   = data['user_name']
            password    = data['password']
            nickname    = data['nickname']
            email       = data['email']

            if User.objects.filter(user_name=user_name).exists():
                return JsonResponse({'MESSAGE':'USER_NAME_ALREADY_EXISTS'}, status=409)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'MESSAGE':'EMAIL_ALREADY_EXISTS'}, status=409)

            if len(user_name) < USER_NAME_MIN_LENGTH:
                return JsonResponse({'MESSAGE':'SHORT_ID'}, status=409)
            if len(user_name) > USER_NAME_MAX_LENGTH:
                return JsonResponse({'MESSAGE':'LONG_ID'}, status=409)
            if len(password) < PASSWORD_MIN_LENGTH:
                return JsonResponse({'MESSAGE':'SHORT_PASSWORD'}, status=409)
            
            user = User.objects.create(
                    user_name   = user_name,
                    password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode(),
                    nickname    = nickname,
                    email       = email
                )

            access_token = jwt.encode({'user_id' : user.id}, SECRET_KEY, algorithm=ALGORITHM)

            return JsonResponse({'MESSAGE':'SUCCESS','access_token':access_token}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALID_KEYS'}, status=400)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['birth', 'website', 'about'],
            properties={
                'birth': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                'website': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
                'about': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        operation_description='sign up to make a new account'
    )
    @login_decorator
    def patch(self, request):
        print(request)
        try:
            if not request.body:
                return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)

            data = json.loads(request.body)

            user    = request.user
            birth   = data.get('birth', user.birth)
            website = data.get('website', user.website)
            about   = data.get('about', user.about)

            user.birth      = birth
            user.website    = website
            user.about      = about
            user.save()
    
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'INVALID_KEYS'}, status=400)
