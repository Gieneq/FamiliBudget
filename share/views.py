from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Share
from .serializers import ShareSerializer, ShareSimpleSerializer
from familybudget.pagination import StandardPagination
from userprofile.models import UserProfile


class ShareQueriedViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        params = request.GET
        slug = params.get('slug', None)
        shared_by = params.get('shared_by', None)

        queryset = Share.objects
        if slug:
            queryset = queryset.filter(profile__slug=slug)
        serializer = ShareSimpleSerializer(queryset.all(), many=True, context={'request':request})
        return Response(serializer.data)


class ShareViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    queryset = Share.objects.all()
    serializer_class = ShareSimpleSerializer
    pagination_class = StandardPagination


# class ShareSlugedViewSet(viewsets.ModelViewSet):
#     """
#     A simple ViewSet for listing or retrieving users.
#     """
#
#     queryset = Share.objects.all()
#     serializer_class = ShareSerializer
#     pagination_class = StandardPagination
#     lookup_field = 'slug'
#     lookup_url_kwarg = 'slug'