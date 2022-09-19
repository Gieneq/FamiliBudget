from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserCreateSerializer, UserDestroySerializer, UserEditSerializer, \
    UserChangePasswordSerializer
from .serializers import UserProfileSerializer
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.reverse import reverse


# todo add First/Last name validation capital letter

class StandardPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    max_page_size = 10


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.update({'userprofile_list': reverse('userprofile:userprofile_list', request=request)})
        response.data.update({'user_create': reverse('userprofile:user_create', request=request)})
        return response


@api_view(['GET'])
def user_detail_view(request, *args, slug=None, **kwargs):
    user = get_object_or_404(User, user_profile__slug=slug)
    serializer = UserSerializer(user, many=False, context={'request': request})
    content = serializer.data
    return Response(content)


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserEditView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    lookup_field = 'user_profile__slug'
    # todo redirect after changing of slug


class UserEditPasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserChangePasswordSerializer
    lookup_field = 'user_profile__slug'

# @api_view(['PUT'])
# def user_edit_password_view(request, *args, slug=None, **kwargs):
#     user = get_object_or_404(User, user_profile__slug=slug)
#     serializer = UserSerializer(user, many=False, context={'request': request})
#     content = serializer.data
#     return Response(content)


class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer
    lookup_field = 'user_profile__slug'


class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    pagination_class = StandardPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.update({'user_list': reverse('userprofile:user_list', request=request)})
        return response


class UserProfileDetailView(APIView):
    def get(self, request, *args, slug=None, **kwargs):
        userprofile = get_object_or_404(UserProfile, slug=slug)
        serializeer = UserProfileSerializer(userprofile, many=False, context={'request': request})
        content = serializeer.data
        return Response(content)
