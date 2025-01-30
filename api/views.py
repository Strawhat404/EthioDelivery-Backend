from django.contrib.auth.models import User
from rest_framework import serializers,generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product,Order
from .serializers import ProductSerializer, OrderSerializer
import stripe 
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreatePaymentView(View):
    def post(self,request):
        try:
            data = request.json()
            amount = int(data["amount"])
            
            payment_intent = stripe.PaymentIntent.create(
                amount = amount,
                currency = "usd",
                payment_method_types = ["card"],
            )
            
            payment = Payment.objects.create(
                user = request.user,
                amount = amount /100,
                stripe_payment_intent_id = payment_intent.id,
                status = "PENDING", 
            )
            return JsonResponse({"clientSecret": payment_intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
# class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Serializer for user registration
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Exclude password from being shown in responses

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Only expose essential fields

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)  # Create a user with encrypted password
        return user

# View for user registration
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)  # Parse incoming data
        if serializer.is_valid():
            serializer.save()  # Save valid data to create a user
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return errors if invalid
