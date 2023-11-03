import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DetailView, FormView

from users.models import FavoriteAlbums
from .forms import AddAlbumForm, SearchForm, CommentForm, ContactForm
from .models import Album, Genre, CartItem, Artist, Comment
from .utils import DataMixin, SearchMixin, CommentMixin


class MainPage(DataMixin, ListView):
    template_name = 'vinilboard/main.html'

    def get_queryset(self):
        return Genre.objects.annotate(cnt=Count('albums')).order_by('pk')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(self.request, title='Главная страница')
        context.update(user_context)
        all_albums = [list(Album.objects.filter(genre__genre=genre.genre).select_related('artist', 'genre'))
                      for genre in self.object_list[:4]]
        for ind, val in enumerate(all_albums):
            random.shuffle(val)
            all_albums[ind] = val[:5]
        context['other_genres'] = self.object_list[4:]
        context['all_albums'] = all_albums

        return context


class ShowCatalog(DataMixin, ListView):
    paginate_by = 25
    template_name = 'vinilboard/catalog.html'

    def get_queryset(self):
        catalog = cache.get('catalog')
        if not catalog:
            catalog = Album.objects.all().select_related('artist')
            cache.set('catalog', catalog, 30)
        return catalog

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(self.request, title='Каталог')
        context.update(user_context)

        return context


class ShowGenre(DataMixin, ListView):
    paginate_by = 25
    template_name = 'vinilboard/genre.html'
    allow_empty = False

    def get_queryset(self):
        genre = cache.get(self.kwargs['genre'])
        if not genre:
            genre = Album.objects.select_related('artist', 'genre').filter(genre__slug=self.kwargs['genre'])
            cache.set(self.kwargs['genre'], genre, 30)
        return genre

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(self.request, title=self.object_list[0].genre)
        context.update(user_context)
        context['other_genres'] = Genre.objects.exclude(slug=self.kwargs['genre']).annotate(cnt=Count('albums'))
        return context


class ShowAlbum(CommentMixin, DetailView):
    template_name = 'vinilboard/album.html'
    context_object_name = 'album'
    slug_url_kwarg = 'album'

    def get_object(self, queryset=None):
        return get_object_or_404(Album.objects.select_related('artist', 'genre'), slug=self.kwargs['album'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user_context = self.get_user_context(self.request, self.object)
        context.update(user_context)
        context['other_releases'] = Album.objects.filter(
            artist__artist=self.object.artist).exclude(slug=self.object.slug).select_related('artist')

        # Если пользователь авторизован получаем количество пластинок в корзине и проверяем, добавлена ли пластинка
        # в избранное
        if self.request.user.is_authenticated:
            context['like'] = FavoriteAlbums.objects.filter(album=self.object, user=self.request.user).exists()
            if user_cart := CartItem.objects.filter(album=self.object, user=self.request.user.id):
                context['user_cart'] = user_cart[0].quantity
            else:
                context['user_cart'] = 0
        return context

    # Метод для обработки отзыва к альбому
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.album = Album.objects.get(slug=self.kwargs['album'])
            comment.save()

            return redirect(comment.album)


class ShowArtist(DataMixin, ListView):
    template_name = 'vinilboard/artist.html'
    context_object_name = 'albums'
    allow_empty = False

    def get_queryset(self):
        return Album.objects.filter(artist__slug=self.kwargs['artist']).select_related('artist')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['artist'] = context['albums'][0].artist
        user_context = self.get_user_context(self.request, title=context['artist'])
        context.update(user_context)

        return context


class AddAlbumView(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddAlbumForm
    template_name = 'vinilboard/add_album.html'
    success_url = reverse_lazy('main')
    permission_required = 'vinilboard.add_album'  # <приложение>.<действие>_<таблица>


class Search(SearchMixin, View):

    def get(self, request):
        if request.GET.get('page') and request.GET.get('keyword'):
            keyword = request.GET.get('keyword')
            context = self.get_user_context(keyword, request, title='Поиск')
            return render(request, 'vinilboard/search.html', context)
        else:
            return redirect('main')

    def post(self, request):
        form = SearchForm(request.POST)  # Получение данных из POST-запроса
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            context = self.get_user_context(keyword, request, title='Поиск')
            return render(request, 'vinilboard/search.html', context)
        else:
            # Данные формы недействительны, возвращаем форму с ошибками
            return render(request, 'vinilboard/search.html', {'form': form})


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'vinilboard/contact.html'
    success_url = reverse_lazy('main')
    # title_page = "Обратная связь"

    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     return super().form_valid(form)




# class CommentCreateView(CreateView):
#     model = Comment
#     template_name = 'vinilboard/album.html'
#     form_class = CommentForm
#
#     def form_valid(self, form):
#         comment = form.save(commit=False)
#         comment.user = self.request.user
#         comment.album = Album.objects.get(slug=self.kwargs['album'])
#         comment.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return self.request.META.get('HTTP_REFERER')


# def search(request):
#     if request.method == 'POST':
#         sf = SearchForm(request.POST)
#         if sf.is_valid():
#             keyword = sf.cleaned_data['keyword']
#             albums = Album.objects.filter(Q(title__icontains=keyword) | Q(artist__artist__icontains=keyword)).\
#                 select_related('artist')
#             paginator = Paginator(albums, per_page=25)
#             page_number = request.GET.get('page', 1)
#             context = {'form': SearchForm(),
#                        'albums': albums}
#     else:
#         return redirect('main')
#     return render(request, 'vinilboard/search.html', context)
