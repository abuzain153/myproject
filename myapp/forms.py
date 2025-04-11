from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'product_code', 'quantity', 'unit', 'min_stock']
        widgets = {
            'quantity': forms.NumberInput(attrs={'step': 'any'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        try:
            float(quantity)  # التحقق من أن القيمة رقم صالح
        except ValueError:
            raise forms.ValidationError("الكمية يجب أن تكون رقمًا صالحًا.")
        return quantity

    def clean_min_stock(self):
        min_stock = self.cleaned_data['min_stock']
        if min_stock <= 0:
            raise forms.ValidationError("الحد الأدنى يجب أن يكون أكبر من صفر.")
        return min_stock
