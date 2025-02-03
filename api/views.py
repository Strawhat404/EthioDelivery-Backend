from django.contrib.auth.models import User
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Product, Order, Cart, CartItem, Payment, Restaurant, Grocery, OtherService, NearbyPick
from .serializers import (
    ProductSerializer, OrderSerializer, CartSerializer, CartItemSerializer,
    RestaurantSerializer, GrocerySerializer, OtherServiceSerializer, NearbyPickSerializer,
    RegisterSerializer
)
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View

stripe.api_key = settings.STRIPE_SECRET_KEY

# Payment View
class CreatePaymentView(View):
    def post(self, request):
        try:
            data = request.json()
            amount = int(data["amount"])

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method_types=["card"],
            )

            payment = Payment.objects.create(
                user=request.user,
                amount=amount / 100,
                stripe_payment_intent_id=payment_intent.id,
                status="PENDING",
            )
            return JsonResponse({"clientSecret": payment_intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Cart Views
class CartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.objects.get(user=self.request.user)

class CartItemView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

# Order Views
class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

# User Registration View
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Restaurant Views
class RestaurantListView(generics.ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

# Grocery Views
class GroceryListView(generics.ListAPIView):
    queryset = Grocery.objects.all()
    serializer_class = GrocerySerializer

# OtherService Views
class OtherServiceListView(generics.ListAPIView):
    queryset = OtherService.objects.all()
    serializer_class = OtherServiceSerializer

# NearbyPick Views
class NearbyPickListView(generics.ListAPIView):
    queryset = NearbyPick.objects.all()
    serializer_class = NearbyPickSerializer