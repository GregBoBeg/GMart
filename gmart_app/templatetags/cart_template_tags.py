from django import template
from gmart_app.models import Order

# Got this idea from:  https://youtu.be/ex6YznLrmSQ?t=814

register = template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(Order_User=user, Order_Ordered=False)
        if qs.exists():
            return qs[0].Order_Product.count()
    return 0
