from .models import Cart

def cart_count(request):
    if request.session.get('uid'):
        cart_count = Cart.objects.filter(user=request.session.get('uid')).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}
