from django.db import models
from mainapp.models import Products
from users.models import User


# Create your models here.

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'basket for {self.user.username} || Product {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    @staticmethod
    def total_quantity(user):
        baskets = Basket.objects.filter(user=user)
        return sum(basket.quantity for basket in baskets)

    @staticmethod
    def total_sum(user):
        baskets = Basket.objects.filter(user=user)
        return sum(basket.sum() for basket in baskets)
