from django.db.models import F, Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from orders.forms import OrderForm
from orders.models import OrderItem
from vinilboard.models import CartItem


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    # title = 'Store | Оформление заказа'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_cart'] = CartItem.objects.filter(user=self.request.user)

        return context

    def form_valid(self, form):
        order = form.save(commit=False)
        order.user = self.request.user
        user_cart = CartItem.objects.filter(user=self.request.user)
        items = user_cart.annotate(sum=F('quantity') * F('album__price'))
        order.total_price = items.aggregate(total_price=Sum('sum'))['total_price']
        order.save()

        for item in user_cart:
            OrderItem.objects.create(order=order, album=item.album, quantity=item.quantity, price=item.album.price)

        return redirect(reverse_lazy('order_create'))
