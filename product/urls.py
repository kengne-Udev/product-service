from django.urls import path
from .views import ProductListCreateAPIView, ProductDetailsAPIView


urlpatterns = [
    path('', ProductListCreateAPIView.as_view(), name='products'),
    path('<int:pk>', ProductDetailsAPIView.as_view(), name='product'),
]
