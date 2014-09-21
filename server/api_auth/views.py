from django.contrib.auth import login, logout

from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class AuthView(APIView):
    authentication_classes = (BasicAuthentication,)

    def post(self, request, *args, **kwargs):
        login(request, request.user)
        return Response(UserSerializer(request.user).data)

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class UserPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method == 'POST' or
                request.user and request.user.is_authenticated())


class UserView(APIView):
    permission_classes = (UserPermission,)

    def get(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data)

    def post(self, request, *args, **kwargs):
        # TODO: registration through email confirmation?
        serialized = UserSerializer(data=request.DATA)
        if serialized.is_valid():
            user = serialized.save()
            return Response(UserSerializer(user).data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serialized._errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
