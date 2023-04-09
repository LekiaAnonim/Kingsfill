from django.db import models
from datetime import date
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Shop(models.Model):
    user = models.OneToOneField(User, null=True, related_name = 'user', on_delete=models.SET_NULL)
    shop_name = models.CharField(max_length=500, null=True, blank=True, default="Shop 1", unique=True)
    date_created = models.DateField(null=True, default=date.today)
    location = models.CharField(max_length=500, null=True, blank=True)
    shop_manager = models.CharField(max_length=500, null=True, blank=True)
    manager_phone = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.shop_name}-{self.id}"
    
    class Meta:

        ordering =['shop_name','-date_created',]

    def get_absolute_url(self):
        return reverse('GasApp:shop-batches', kwargs={'id': self.id})
    
class Batch(models.Model):
    shop = models.ForeignKey(Shop, related_name='shop', on_delete=models.SET_NULL, null=True)
    batch_name = models.CharField(max_length=500, null=True, blank=True, default="Batch", unique=True)
    date_created = models.DateField(null=True, default=date.today)
    cost = models.DecimalField(null=True, max_digits=20, decimal_places=2)
    kg = models.DecimalField(null=True, max_digits=20, decimal_places=2)
    price_per_kg = models.DecimalField(null=True, blank=True, max_digits=20, decimal_places=2)
    vendor_name = models.CharField(max_length=500, null=True, blank=True)
    vendor_phone = models.CharField(max_length=500, null=True, blank=True)
    close_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.batch_name}"

    def get_id(self):
        return self.id
    
    class Meta:

        ordering =['-date_created',]
        verbose_name_plural = "Batches"

    def get_absolute_url(self):
        return reverse('GasApp:batch-sales', kwargs={'shop_id': self.shop.id, 'id': self.id})


class Sale(models.Model):
    batch = models.ForeignKey(Batch, related_name='batch', on_delete=models.SET_NULL, null=True)
    kg = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    price = models.DecimalField(null=True, max_digits=20, decimal_places=2)
    date = models.DateField(null=True, default=date.today)
    customer_name = models.CharField(max_length=500, null=True, blank=True)
    customer_phone = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.id}-{self.customer_name}-{self.date}-{self.kg}"
    
    class Meta:

        ordering =['-date',]
        verbose_name_plural = "Sales"

    def get_absolute_url(self):
        return reverse('GasApp:sale-receipt', kwargs={'pk': self.id})