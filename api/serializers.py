from rest_framework import serializers
from .models import Product, Order, Cart, CartItem,OrderItem



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id','product','quantity' ]
        
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many= True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ['id','user','items', 'created_at', 'updated_at']