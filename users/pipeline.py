from django.contrib.auth.models import Group, Permission


def new_users_handler(backend, user, response, *args, **kwargs):
    """Добавляет пользователя, который авторизовывается через соц. сети,
    в группу Social"""

    group = Group.objects.filter(name='social')
    if len(group):
        user.groups.add(group[0])



