from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from product.models import Products_in_storage


class Delivers(models.Model):
    amount = models.IntegerField()
    OPTIONS = (
        ('Подготовка к отправке', 'Подготовка к отправке'),
        ('В пути', 'В пути'),
        ('Прибыл в пункт назначения', 'Прибыл в пункт назначения'),
    )
    product = models.ForeignKey(Products_in_storage, on_delete=models.SET_NULL, null=True, related_name="deliver_product")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, choices=OPTIONS)

    def __str__(self):
        return f'{self.product}  {self.user}  {self.status}'


# Сигналы для автоматического изменения количества товара при изменении статуса доставки


@receiver(post_save, sender=Delivers)
def update_product_amount(sender, instance, **kwargs):
    if instance.status == 'Прибыл в пункт назначения':
        product = instance.product
        product.amount += instance.amount
        product.save()
