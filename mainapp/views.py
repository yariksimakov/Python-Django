from django.shortcuts import render
import os, json
from mainapp import models


dir = os.path.dirname(__file__)

# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    file_path = os.path.join(dir, 'fixtures/fixtures.json')
    context = {
        "title": "geekshop",
        "categorys": models.ProductsCategory.objects.all(),
        "products": models.Products.objects.all()

    }

    return render(request, 'mainapp/products.html', context)


