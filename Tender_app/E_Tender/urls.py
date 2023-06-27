from django.urls import path
from .views import BidCreateAPIView

urlpatterns = [
    path('bid/', BidCreateAPIView.as_view(), name='bid-create'),
]