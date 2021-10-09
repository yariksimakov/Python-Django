from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from mainapp.models import Products, ProductsCategory


# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


def products(request, category_id=None, page_id=1):
    products = Products.objects.filter(
        category=category_id) if category_id != None else Products.objects.all()
    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page_id)

    except PageNotAnInteger:
        products_paginator = paginator.page(1)

    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        "title": "geekshop",
        "categorys": ProductsCategory.objects.all(),
        "products": products_paginator,
    }

    return render(request, 'mainapp/products.html', context)
