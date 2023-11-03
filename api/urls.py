from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.views import AlbumModelViewSet, ArtistModelViewSet, GenreModelViewSet

router = DefaultRouter()

router.register(r'albums', AlbumModelViewSet)
router.register(r'artists', ArtistModelViewSet)
router.register(r'genres', GenreModelViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('albums/', AlbumModelViewSet.as_view({'get': 'list'})),
    # path('artist/', ArtistModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('artist/<int:pk>', ArtistModelViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]
