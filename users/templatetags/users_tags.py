from django import template

register = template.Library()


@register.inclusion_tag('users/profile_menu.html')
def profile_menu(title=None):
    menu = [
        {'name': 'Профиль', 'url': 'profile'},
        {'name': 'Мои заказы', 'url': 'user_orders'},
        {'name': 'Избранные пластинки', 'url': 'favorites'},
        {'name': 'Корзина', 'url': 'cart'}
    ]
    return {'menu': menu, 'title': title}
