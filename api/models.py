from django.db import models
from django.contrib.auth.models import User

# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField() 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Delivered', 'Delivered'),    
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)  
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) 

    def __str__(self):
        return f"Order {self.id} - {self.status}"

# Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    items = models.ManyToManyField(Product, through='CartItem')  

    def __str__(self):
        return f"Cart for {self.user.username}"

# CartItem Model (Intermediate table for Cart and Product)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField(default=1)   

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in cart"
