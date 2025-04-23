from django import forms
from .models import Product, StockMovement

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['product_id']
        fields = '__all__'
        widgets = {
            'product_id': forms.TextInput(attrs={'readonly': 'readonly'})
        }

class StockMovementForm(forms.ModelForm):
    class Meta:
        model = StockMovement
        fields = ['product', 'movement_type', 'quantity']
