from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

urlpatterns = [
    path('', cache_page(10)(ShowCatalog.as_view()), name='catalog'),
    path('search/', Search.as_view(), name='search'),
    path('add_album/', AddAlbumView.as_view(), name='add_album'),
    path('<genre>/', cache_page(10)(ShowGenre.as_view()), name='genre'),
    path('artists/<artist>/', cache_page(10)(ShowArtist.as_view()), name='artist'),
    path('albums/<slug:album>/', cache_page(10)(ShowAlbum.as_view()), name='album'),
    # path('add_to_cart/<slug:album_slug>/<int:add>/', add_to_cart, name='add_to_cart_from_catalog'),
    # path('albums/add_comment/<slug:album>/', CommentCreateView.as_view(), name='comment'),
]