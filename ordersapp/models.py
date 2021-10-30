from django.db import models

# Create your models here.
from geekshop import settings
from mainapp.models import Products


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    CHOICES_STATUS = (
        (FORMING, 'ФОРМИРУЕТСЯ'),
        (SEND_TO_PROCEED, 'ОТПРАВЛЕН В ОБРАБОТКУ'),
        (PAID, 'ОПЛАЧЕНО'),
        (PROCEEDED, 'ОБРАБАТЫВАЕТСЯ'),
        (READY, 'ГОТОВ К ВЫДАЧИ'),
        (CANCEL, 'ОТМЕНА ЗАКАЗА'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    update = models.DateTimeField(verbose_name='обновлен', auto_now=True)
    status = models.CharField(choices=CHOICES_STATUS, verbose_name='статус', max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __str__(self):
        return f'текущий закказ {self.pk}'

    def get_total_quantity(self):
        receiver = self.orderitems.select_related()
        return sum(list(map(lambda param: param.quantity, receiver)))

    def get_total_cost(self):
        receiver = self.orderitems.select_related()
        return sum(list(map(lambda element: element.get_product_cost(), receiver)))

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for element in self.orderitems.sellect_related():
            element.product.quantity += element.quantity
            element.save()
        self.is_active = False
        self.save()


class OrderItems(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='колличество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
