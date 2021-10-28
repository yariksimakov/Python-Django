from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from baskets.models import Basket
from ordersapp.forms import OrderItemsForm
from ordersapp.models import Order, OrderItems


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop | Создать заказ'

        OrderSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=1)

        if self.request.POST:
            formset = OrderSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items:
                OrderSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=basket_items.count())
                formset = OrderSet()

                for num, form in enumerate(formset.forms):
                    form.fields['product'] = basket_items[num].product
                    form.fields['quantity'] = basket_items[num].quantity
                    form.fields['price'] = basket_items[num].price
                basket_items.delete()
            else:
                formset = OrderSet()

        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderCreate, self).form_valid(form)





class OrderUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context['title'] = 'GeeksShop | обновить заказ'

        OrderSet = inlineformset_factory(Order, OrderItems, form=OrderItemsForm, extra=1)

        if self.request.POST:
            form_set = OrderSet(self.request.POST, instance=self.object)
        else:
            form_set = OrderSet(instance=self.object)
            for form in form_set:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = form_set
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        order_item = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if order_item.is_valid():
                order_item.instance = self.object
                order_item.save()

            if self.object.get_total_cost() == 0:
                self.object.delete()
        return super(OrderUpdate, self).form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('orders:list')


class OrderDetail(DetailView):
    model = Order
    title = 'GeekShop | Просмотр заказов'


def order_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SEND_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order:list'))
