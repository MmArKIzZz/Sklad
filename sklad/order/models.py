from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from product.models import Products_in_storage

class OrderOut(models.Model):
    OPTIONS = (
        ('На рассмотрении', 'На рассмотрении'),
        ('Подготовка к отправке', 'Подготовка к отправке'),
        ('В пути', 'В пути'),
        ('Прибыл в пункт назначения', 'Прибыл в пункт назначения'),
    )
    product = models.ForeignKey(Products_in_storage, on_delete=models.SET_NULL, null=True, related_name="order_out_product")
    amount = models.IntegerField()
    worker = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="order_out_worker")  # Поле worker для выбора пользователей из группы "work"
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="order_out_user")  # Поле user для выбора пользователя
    status = models.CharField(max_length=50, choices=OPTIONS)

    def clean(self):
        if self.amount > self.product.amount:
            raise ValidationError("Выбранное количество превышает количество продукта на складе.")

    def __str__(self):
        return f'{self.product}  {self.user} {self.status}'

# Сигналы для автоматического уменьшения количества товара при изменении статуса заказа


@receiver(post_save, sender=OrderOut)
def update_product_amount(sender, instance, **kwargs):
    if instance.status == 'Подготовка к отправке':
        product = instance.product
        product.amount -= instance.amount
        product.save()



