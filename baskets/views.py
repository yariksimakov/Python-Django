from django.shortcuts import render


from django.shortcuts import HttpResponseRedirect
from mainapp.models import Products
from baskets.models import Basket
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def basket_add(request, product_id):
    user_select = request.user
    product = Products.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=user_select, product=product)
    if not baskets.exists():
        Basket.objects.create(user=user_select, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, product_id):
    Basket.objects.get(id=product_id).delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
