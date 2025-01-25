from django.contrib.auth.models import User
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
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
