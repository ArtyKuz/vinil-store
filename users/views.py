from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Sum, Q, F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView

from users.forms import LoginUserForm, RegisterUserForm, UserProfileForm, UserPasswordChangeForm, ImageForm
from users.models import Profile, FavoriteAlbums
from vinilboard.forms import SearchForm
from vinilboard.models import Album, CartItem
from vinilboard.utils import DataMixin


class RegisterUser(SuccessMessageMixin, DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('login')
    success_message = 'Вы успешно зарегистрированы!'
    title = 'Регистрация'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.request, **kwargs)

        return context


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    title = 'Вход'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(self.request, **kwargs)

        return context


def logout_user(request):
    logout(request)
    return redirect('main')


class UserProfileView(LoginRequiredMixin, DataMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    login_url = 'login'
    title = 'Профиль'

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(self.request, **kwargs)
        context['image_form'] = ImageForm

        return context


class UserCart(LoginRequiredMixin, DataMixin, ListView):
    paginate_by = 25
    template_name = 'users/cart.html'
    context_object_name = 'user_cart'
    login_url = 'login'
    title = 'Корзина'

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user).select_related('album', 'album__artist').annotate(
            sum=F('quantity') * F('album__price'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(self.request, **kwargs)
        order_price = self.object_list.aggregate(order_price=Sum('sum'))
        context.update(order_price)

        return context


def add_to_cart(request, album_slug, add):
    album = Album.objects.get(slug=album_slug)
    # Проверяем, есть ли уже запись о данной пластинке в корзине
    cart_item, created = CartItem.objects.get_or_create(album=album, user=request.user)

    if not created:
        # Если запись уже существует
        if add:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity -= 1
            cart_item.save()
            if cart_item.quantity == 0:
                cart_item.delete()
    return redirect(request.META['HTTP_REFERER'])


def add_to_favorite(request, album_id, add):
    album = Album.objects.get(pk=album_id)
    if add:
        album = Album.objects.get(pk=album_id)
        FavoriteAlbums.objects.create(album=album, user=request.user)
    else:
        FavoriteAlbums.objects.get(album=album, user=request.user).delete()
    return redirect(request.META['HTTP_REFERER'])


class UserOrders(ListView):
    pass


class UserFavorites(DataMixin, ListView):
    model = FavoriteAlbums
    template_name = 'users/favorite_albums.html'
    context_object_name = 'favorite_albums'
    title = 'Избранные пластинки'

    def get_queryset(self):
        return FavoriteAlbums.objects.select_related('album').filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(self.request, **kwargs)

        return context


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'users/password_change_form.html'


class ImageFormView(CreateView):
    form_class = ImageForm

    def form_valid(self, form):
        try:
            user = Profile.objects.get(user=self.request.user)
            user.image = form.cleaned_data['image']
            user.save()
        except ObjectDoesNotExist:
            user = form.save(commit=False)
            user.user = self.request.user
            user.save()
        return redirect('profile')


