from django.db import models
from django.contrib.auth import get_user_model
# from django.utils import timezone

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=200, null=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.category_name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # category = models.CharField(max_length=200, null=True)
    quantity = models.PositiveIntegerField(null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, max_length=11, null=True)
    image = models.ImageField(default='product_avatar.png', upload_to='Product_Images')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

status = (
    ('Pending', 'Pending'),
    ('Canceled', 'Canceled'),
    ('Confirmed', 'Confirmed'),
    ('Delivered', 'Delivered'),
)

class Order(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, max_length=11, null=True)
    quantity = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=11, choices=status, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    ordered_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, max_length=11, null=True)
    


    def __str__(self):
        return self.product_id.name
