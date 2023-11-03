from django.contrib.auth.views import PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path

from users.views import *


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('cart/', UserCart.as_view(), name='cart'),
    path('add_to_cart/<slug:album_slug>/<int:add>/', add_to_cart, name='add_to_cart'),
    path('add_to_favorites/<int:album_id>/<int:add>/', add_to_favorite, name='add_to_favorite'),
    path('orders/', UserOrders.as_view(), name='orders'),
    path('favorites/', UserFavorites.as_view(), name='favorites'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('password-change/', UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'), name='password_change_done'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html'), name='password_reset'),
    path('password-reset/done', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('change-image/', ImageFormView.as_view(), name='change_image'),

]
