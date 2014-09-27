from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

import jwt
from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import (jwt_payload_handler,
                                            jwt_encode_handler,
                                            jwt_decode_handler)

from .models import APIUser
from .serializers import UserSerializer


class ConfirmationView(UpdateAPIView):
    model = APIUser
    serializer_class = UserSerializer

    def decode_token(self, data):
        token = data.get('token', '')
        try:
            data = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed('Signature has expired.')
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Error decoding signature.')
        else:
            return data

    def get_serializer(self, instance, data, *args, **kwargs):
        data = self.decode_token(data)
        return super(ConfirmationView, self).get_serializer(
            instance=instance, data=data, *args, **kwargs)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.filter_queryset(self.get_queryset())
        data = self.decode_token(self.request.DATA)
        email = data['email']
        obj = get_object_or_404(queryset, email=email)
        self.check_object_permissions(self.request, obj)
        return obj


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method == 'POST' or
                request.user and request.user.is_authenticated())


class EmailConfirmationMixin(object):
    subject = '[antxetamedia.info] Registration confirmation'
    template_name = 'api_auth/confirmation.txt'

    def build_token(self, user):
        jwt = jwt_payload_handler(user)
        jwt['password'] = user.password
        return jwt_encode_handler(jwt)

    def send_confirmation_email(self, user):
        token = self.build_token(user)
        ctx = {'user': user, 'token': token}
        body = render_to_string(self.template_name, ctx)
        send_mail(self.subject, body, settings.DEFAULT_FROM_EMAIL,
                  [user.email], fail_silently=False)


class UserView(APIView, EmailConfirmationMixin):
    permission_classes = (UserPermission,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            self.send_confirmation_email(serialized.object)
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response(serialized._errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            serialized.save()
            return Response({}, status=status.HTTP_200_OK)
        else:
            return Response(serialized._errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
