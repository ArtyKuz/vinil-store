from django.core.paginator import Paginator
from django.db.models import Count, Q, Sum

from .forms import SearchForm, CommentForm
from .models import *


class DataMixin:

    def get_user_context(self, request, **kwargs):
        context = kwargs
        if 'users' not in request.path:
            context['search_form'] = SearchForm()

        return context


class SearchMixin(DataMixin):

    def get_user_context(self, keyword, request, **kwargs):
        context = super().get_user_context(request, **kwargs)
        albums = Album.objects.filter(
            Q(title__icontains=keyword) | Q(artist__artist__icontains=keyword)).select_related('artist')
        paginator = Paginator(albums, per_page=25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        context['keyword'] = keyword

        return context


class CommentMixin(DataMixin):

    def get_user_context(self, request, album: Album):
        context = super().get_user_context(request, title=album)
        comments = album.get_comments()
        if request.user.is_authenticated:
            context['comment_form'] = CommentForm()
        if comments:
            avg_mark = comments.aggregate(avg_mark=Avg('mark'))['avg_mark']
            context['comments'] = comments
            context['avg_mark'] = round(avg_mark, 1)
            paginator = Paginator(comments, per_page=5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context['paginator'] = paginator
            context['page_obj'] = page_obj

        return context
