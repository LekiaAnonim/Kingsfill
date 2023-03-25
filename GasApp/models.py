from django.db import models
from datetime import date
from django.urls import reverse
# Create your models here.
class Batch(models.Model):
    batch_name = models.CharField(max_length=500, null=True, blank=True, default="Batch"+str(id))
    date_created = models.DateField(null=True, default=date.today)
    cost = models.DecimalField(null=True, decimal_places=2)
    kg = models.DecimalField(null=True, decimal_places=2)
    price_per_kg = models.DecimalField(null=True, decimal_places=2)
    vendor_name = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.batch_name}"
    
    class Meta:

        ordering =['-date_created',]
        verbose_name_plural = "Batches"

    def get_absolute_url(self):
        return reverse('batch_detail', kwargs={'id': self.id})


class Sale(models.Model):
    kg = models.DecimalField(null=True, decimal_places=2)
    price = models.DecimalField(null=True, decimal_places=2)
    date = models.DateField(null=True, default=date.today)
    customer_name = models.CharField(max_length=500, null=True, blank=True)
    customer_phone = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.batch_name}"
    
    class Meta:

        ordering =['-date',]
        verbose_name_plural = "Sales"

    def get_absolute_url(self):
        return reverse('sale_detail', kwargs={'id': self.id})