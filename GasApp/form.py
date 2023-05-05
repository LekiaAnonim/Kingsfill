from django import forms
from .models import Batch, Sale, Shop
class SaleForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kg'].widget.attrs.update({'placeholder': 'No. of kg'})
        self.fields['price'].widget.attrs.update({'placeholder': 'Price'})
        self.fields['date'].widget.attrs.update({'placeholder': 'Date'})
        self.fields['customer_name'].widget.attrs.update({'placeholder': 'Customer name'})
        self.fields['customer_phone'].widget.attrs.update({'placeholder': 'Customer phone number'})
    class Meta:
        model = Sale
        fields = ('kg', 'price', 'payment_type', 'date', 'customer_name', 'customer_phone')

class BatchForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['kg'].widget.attrs.update({'placeholder': 'No. of kg'})
        self.fields['cost'].widget.attrs.update({'placeholder': 'Cost'})
        self.fields['price_per_kg'].widget.attrs.update({'placeholder': 'Price per kg'})
        self.fields['vendor_name'].widget.attrs.update({'placeholder': 'Vendor name'})
        self.fields['vendor_phone'].widget.attrs.update({'placeholder': 'Vendor phone number'})
    class Meta:
        model = Batch
        fields = ('shop', 'batch_name', 'date_created', 'cost', 'kg', 'price_per_kg', 'vendor_name','vendor_phone', 'close_account')

class ShopForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['shop_name'].widget.attrs.update({'placeholder': 'Name of shop'})
        self.fields['location'].widget.attrs.update({'placeholder': 'Shop location'})
        # self.fields['date_created'].widget.attrs.update({'placeholder': 'Enter date'})
        self.fields['shop_manager'].widget.attrs.update({'placeholder': 'Full name of shop manager'})
        self.fields['manager_phone'].widget.attrs.update({'placeholder': 'Manager phone number'})
    class Meta:
        model = Shop
        fields = ('user','shop_name', 'location', 'shop_manager', 'manager_phone', 'date_created')