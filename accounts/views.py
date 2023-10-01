from django.shortcuts import render

from rest_framework import generics, status, views, permissions
from rest_framework.permissions import IsAuthenticated
from accounts.serializer import RegisterSerializer, \
    EmailVerificationSerializer, LoginSerializer, LogoutSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from django.conf import settings

from .models import Users
from .renders import UserRenderer
import json
from django.urls import reverse
from .utils import Util
from django.http import HttpResponsePermanentRedirect, HttpResponse
import os


class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        print(token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(payload)
        user = Users.objects.get(id=payload['user_id'])
        print(user)
        try:
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


'''

User can register with this view send email to user for verify email

'''


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        users = Users.objects.all()
        serializer = RegisterSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            user = Users.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            # current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://130.185.120.115:3000//authentication/email-verify' + relativeLink + "?token=" + str(token)
            email_body = 'Hi ' + user.email + \
                         ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data)
            return HttpResponse(json.dumps(user_data), content_type='/localhost:3000/email-verify/')


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user.id
        print(user)
        serializer = LoginSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = Users.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
