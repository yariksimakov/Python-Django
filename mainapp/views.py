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


# def test(request):
#     # shirt code
#     context = {
#         'title': 'geekshop',
#         'header': 'Wellcome on the cite',
#         'user': 'User_name',
#         'fixtures': [
#             {'name': 'Худи черного цвета с монограммами adidas Originals', 'price': '6 090,00'},
#             {'name': 'Синяя куртка The North Face', 'price': '23 725,00'},
#             {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN', 'price': '3 390,00'},
#         ],
#         'products_promo': [
#             {'name': 'Черный рюкзак Nike Heritage', 'price': '1875'}
#         ]
#     }
#     return render(request, 'mainapp/test.html', context)