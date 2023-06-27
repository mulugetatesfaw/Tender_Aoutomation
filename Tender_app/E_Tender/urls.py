from django.urls import path
from .views import BidCreateAPIView,VendorCreateAPIView,TenderCreateAPIView

urlpatterns = [
    path('vendor/', VendorCreateAPIView.as_view(), name='post_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='post_tender'),
    path('bid/', BidCreateAPIView.as_view(), name='post_bid'),
]