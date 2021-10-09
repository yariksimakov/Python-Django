from django.shortcuts import render
import os, json
from mainapp import models


# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    context = {
        "title": "geekshop",
        "categorys": models.ProductsCategory.objects.all(),
        "products": models.Products.objects.all()

    }

    return render(request, 'mainapp/products.html', context)
