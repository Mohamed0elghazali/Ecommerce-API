from django.db import models
from django.contrib.auth.models import User

from operator import mod

from product.models import Product

class OrderStatus(models.TextChoices):
    PROCESSING = "Processing"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

class PaymentStatus(models.TextChoices):
    PAID = "Paid"
    UNPAID = "Unpaid"

class PaymentMethod(models.TextChoices):
    COD = "COD" # cash on delivery
    CARD = "Card"


class Order(models.Model):
    city = models.CharField(max_length=100, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=100, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=100, default="", blank=False)
    total_amount = models.IntegerField(default=0)
    payment_method = models.CharField(max_length=30, choices=PaymentMethod.choices)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices)
    status = models.CharField(max_length=30, choices=OrderStatus.choices)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    
class OrderItems(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=False)

    def __Str__(self):
        return self.name    
