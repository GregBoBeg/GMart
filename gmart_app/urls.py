# gmart_app URL Configuration

from django.urls import path
from .views import HomeView, add_to_cart, remove_from_cart
from . import views

# The urlpatterns list below routes URLs to their corresponding views.

urlpatterns = [
    path('', HomeView.as_view(), name='gmart-home'),
    path('about/', views.about, name='gmart-about'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='gmart-product-detail'),
    path('add_to_cart/<int:pk>/<int:addQty>', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<int:pk>/<int:cart>', remove_from_cart, name='remove-from-cart'),
    path('gmart-cart/<int:pk>', views.OrderItemView.as_view(), name='gmart-cart'),
]
