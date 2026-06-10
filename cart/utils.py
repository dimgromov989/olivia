from .models import Cart, CartItem


def get_or_create_cart(request):
    guest_id = request.COOKIES.get("guest_cart_id")
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, session_id=None)
        if guest_id and not created:
            guest_cart = Cart.objects.filter(session_id=guest_id, user=None).first()
            if guest_cart:
                for item in guest_cart.items.all():
                    cart_item, _ = CartItem.objects.get_or_create(
                        cart=cart, product=item.product, defaults={"quantity": 0}
                    )
                    cart_item.quantity += item.quantity
                    cart_item.save()
                guest_cart.delete()

        return cart
    else:
        cart, created = Cart.objects.get_or_create(session_id=guest_id, user=None)
        return cart
