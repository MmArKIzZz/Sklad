from django.db import models

class Products_in_storage(models.Model):
    amount = models.IntegerField()
    name = models.CharField(max_length=50)
    discription =  models.CharField(max_length=500,blank=True)

    def __str__(self):
        return f'{self.name}  {self.amount}'