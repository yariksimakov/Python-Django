from django.shortcuts import render
import os, json


dir = os.path.dirname(__file__)

# Create your views here.
def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    file_path = os.path.join(dir, 'fixtures/fixtures.json')
    context = {
        "title": "geekshop",
        "products": json.load(open(file_path, encoding='utf-8'))
    }

    return render(request, 'mainapp/products.html', context)


