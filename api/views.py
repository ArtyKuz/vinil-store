from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAdminUser

from vinilboard.models import Album, Artist, Genre
from api.serializers import AlbumSerializer, ArtistSerializer, ArtistAddSerializer, GenreSerializer


class Pagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class AlbumModelViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminOrReadOnly]

    # def get_permissions(self):
    #     if self.action in ('create', 'update', 'destroy'):
    #         self.permission_classes = (IsAdminUser,)
    #     return super().get_permissions()


class ArtistModelViewSet(ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        if self.action in ('list', 'retrieve'):
            self.serializer_class = ArtistSerializer
        elif self.action in ('create', 'update'):
            self.serializer_class = ArtistAddSerializer
        kwargs.setdefault('context', super().get_serializer_context())
        return self.serializer_class(*args, **kwargs)


class GenreModelViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
