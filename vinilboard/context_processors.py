from django.db.models import Sum, Q

from vinilboard.models import CartItem


def user_cart(request) -> dict:
    """Функция создающая глобальную переменную cart для использования ее в контексте,
    для этого необходимо подключить данную функцию в settings TEMPLATES (context_processors)"""

    user = request.user
    if user.is_authenticated:
        result: dict = CartItem.objects.aggregate(cart=Sum('quantity', filter=Q(user=request.user)))
        if result['cart']:
            return result
    return {'cart': 0}
