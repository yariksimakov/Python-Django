from django.core.management.base import BaseCommand
from mainapp.models import ProductsCategory, Products
from django.contrib.auth.models import User

import json, os

JSON_PATH = 'mainapp/fixtures'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf-8') as infile:
        return json.load(infile)

class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categorys')

        ProductsCategory.objects.all().delete()
        for category in categories:
            cat = category.get('fields')
            cat['id'] = category.get('pk')
            new_category = ProductsCategory(**cat)
            new_category.save()

        products = load_from_json('products')

        Products.objects.all().delete()
        for product in products:
            prod = product.get('fields')
            category_name = prod.get("category")
            # get a category by name
            _category = ProductsCategory.objects.get(id=category_name)
            # replace the category name with an object
            prod['category'] = _category
            new_product = Products(**prod)
            new_product.save()

    # create superuser with the help of a manager
    """ не работает, так как нужно разрешение прописать в settings"""
    # super_user = User.objects.create_superuser('django', 'django@geekshop.local', 'dgeekbrains')


