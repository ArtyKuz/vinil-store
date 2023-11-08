from django.urls import path

from orders.views import OrderCreateView, OrderSuccessView, UserOrdersView

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('order-success/', OrderSuccessView.as_view(), name='order_success'),
    path('history-orders/', UserOrdersView.as_view(), name='user_orders'),
]
