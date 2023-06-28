from django import forms
from .models import Product, Order, Category

class AddProductForm(forms.ModelForm):
    quantity = forms.IntegerField(required=False)
    id = forms.IntegerField(required=False)
    class Meta:
        model=Product
        fields = ['name','category','quantity','image']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product_id','quantity']

class CategoryForm(forms.ModelForm):
    id = forms.CharField(required=False)
    class Meta:
        model = Category
        fields = ['category_name','id']
