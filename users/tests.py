from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.data = {
            'username': 'Lennon',
            'email': 'Lennon@beatles.ru',
            'first_name': 'John',
            'last_name': 'Lennon',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_user_registration_success(self):
        user_model = get_user_model()
        path = reverse('register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(user_model.objects.filter(username=self.data['username']).exists())

    def test_user_registration_password_error(self):
        self.data['password2'] = '12345678A'
        path = reverse('register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают')

    def test_user_registration_exist_error(self):
        user_model = get_user_model()
        user_model.objects.create(username=self.data['username'])
        path = reverse('register')
        response = self.client.post(path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует')
