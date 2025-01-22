from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)  
    description = models.TextField()        
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    stock = models.IntegerField()           
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.name  

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),             
        ('In Transit', 'In Transit'),      
        ('Delivered', 'Delivered'),        
        ('Canceled', 'Canceled'),          
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    created_at = models.DateTimeField(auto_now_add=True)      
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending') 
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    
    def __str__(self):
        return f"Order {self.id} - {self.status}"
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who owns the cart
    products = models.ManyToManyField(Product, through='CartItem')  # Link to products in the cart
    created_at = models.DateTimeField(auto_now_add=True)      # Timestamp for when the cart was created

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"  # Display cart ID and user name when printed
