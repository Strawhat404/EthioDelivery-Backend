from rest_framework_simplejwt.views import(
    TokenObtainPairView, 
    TokenRefreshView,
)
from .views import RegisterView,ProductListCreateView, ProductDetailView
from django.urls import path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name = 'token_refresh'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('products/', ProductListCreateView.as_view(), name = 'product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
]