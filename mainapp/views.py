from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import ListView

from mainapp.models import Products, ProductsCategory


# Create your views here.


def index(request):
    return render(request, 'mainapp/index.html')


class ProductsListView(ListView):

    model = Products
    template_name = 'mainapp/products.html'
    paginate_by = 3

    def get_queryset(self):
        if self.kwargs:
            if 'category_id' in self.kwargs.keys():
                return Products.objects.filter(category=self.kwargs['category_id'])
            elif 'discharge' in self.kwargs.keys():
                return Products.objects.all()
            else:
                return Products.objects.all()
    #
    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['title'] = "geekshop"
        context['categorys'] = ProductsCategory.objects.all()
        list_exam = self.get_queryset()
        paginator = Paginator(list_exam, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            products_pagintor = paginator.page(page)

        except PageNotAnInteger:
            products_pagintor = paginator.page(1)

        except EmptyPage:
            products_pagintor = paginator.page(paginator.num_pages)

        context['products'] = products_pagintor
        return context


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
