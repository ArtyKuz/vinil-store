from django import forms
from django.contrib.auth.models import User

from orders.models import Order


class OrderForm(forms.ModelForm):
    # user = forms.CharField(disabled=True, widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                                           }))

    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Россия, Москва, ул. Мира, дом 6'}),
                              label='Адрес доставки:')

    class Meta:
        model = Order
        fields = ('address',)
