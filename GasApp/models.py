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
        ordering =['shop_name','date_created', 'id']

    def get_absolute_url(self):
        return reverse('GasApp:shop-batches', kwargs={'pk': self.id})

# class Cylinder(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
#     cylinder_capacity = models.DecimalField(max_digits=50, null=True, blank=True, decimal_places=2)
#     cylinder_name = models.CharField(max_length=500, null=True, blank=True, unique=True)

#     def __str__(self):
#         return f"{self.shop.shop_name}-{self.cylinder_name}-{self.cylinder_capacity}"
    
#     class Meta:
#         ordering =['cylinder_name','cylinder_capacity']


    
class Batch(models.Model):
    shop = models.ForeignKey(Shop, related_name='shop', on_delete=models.SET_NULL, null=True)
    # create a many-to-many field for cylinder
    # cylinders = models.ManyToManyField(Cylinder, related_name='cylinders', blank=True)
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
    # create a foreignkey for cylinder
    # cylinder = models.ForeignKey(Cylinder, related_name='cylinder', on_delete=models.SET_NULL, null=True)
    kg = models.DecimalField(null=True,max_digits=20, decimal_places=2)
    price = models.DecimalField(null=True, max_digits=20, decimal_places=2)
    date = models.DateField(null=True, default=date.today)
    customer_name = models.CharField(max_length=500, null=True, blank=True)
    customer_phone = models.CharField(max_length=500, null=True, blank=True)
    PAYMENT_TYPE = (
        ("POS", "POS"),
        ("Cash", "Cash"),
        ("Bank Transfer", "Bank Transfer"),
    )
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE, default="Cash")

    def __str__(self):
        return f"{self.id}-{self.customer_name}-{self.date}-{self.kg}"
    
    class Meta:

        ordering =['-date',]
        verbose_name_plural = "Sales"

    def get_absolute_url(self):
        return reverse('GasApp:sale-receipt', kwargs={'pk': self.id})