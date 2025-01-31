from rest_framework_simplejwt.views import(
    TokenObtainPairView, 
    TokenRefreshView,
)
from .views import RegisterView,ProductListCreateView, ProductDetailView,OrderListCreateView,OrderDetailView
from django.urls import path
from .webhooks import stripe_webhook

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(), name = 'token_refresh'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('products/', ProductListCreateView.as_view(), name = 'product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
]
]