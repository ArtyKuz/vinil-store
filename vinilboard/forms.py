from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *

import datetime


class AddAlbumForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['artist'].empty_label = "Исполнитель не выбран"
        self.fields['genre'].empty_label = "Стиль не выбран"

    class Meta:
        model = Album
        fields = ['artist', 'title', 'slug', 'year', 'label', 'genre', 'price', 'photo']
        widgets = {
            'artist': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'year': forms.NumberInput(attrs={'class': 'form-control'}),
            'label': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_year(self):
        year = self.cleaned_data['year']
        current_year = datetime.datetime.now().year
        if year > current_year:
            raise ValidationError('Год выпуска альбома не должен превышать текущий год')

        return year


class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=50, min_length=2, label='',
                              widget=forms.TextInput(attrs={'class': 'form-control me-3',
                                                            'aria-label': 'Поиск',
                                                            'placeholder': "Поиск"}),
                              error_messages={'min_length': 'Слишком мало символов'})


class CommentForm(forms.ModelForm):
    content = forms.CharField(max_length=1000, min_length=1, label='',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'placeholder': 'Оставить отзыв',
                                                           'style': 'height: 100px'}),
                              error_messages={'min_length': 'Отзыв не может быть пустым',
                                              'max_length': 'Текст отзыва не может превышать 1000 символов'})

    class Meta:
        model = Comment
        fields = ['content', 'mark']
        widgets = {'mark': forms.Select(attrs={'class': 'col-md-2',
                                               })
                   }
        labels = {'mark': 'Ваша оценка'}


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
