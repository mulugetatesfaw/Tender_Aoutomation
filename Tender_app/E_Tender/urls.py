from django.urls import path
from .views import BidCreateAPIView,VendorCreateAPIView,TenderCreateAPIView,GradeCreateAPIView,VendorDeleteAPIView

urlpatterns = [
    # Paths to create models
    path('vendor/', VendorCreateAPIView.as_view(), name='post_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='post_tender'),
    path('bid/', BidCreateAPIView.as_view(), name='post_bid'),
    path('grade/', GradeCreateAPIView.as_view(), name='post_grade'),
    
    # Paths to update an existing data on our models
    path('vendor/', VendorCreateAPIView.as_view(), name='update_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='update_tender'),
    path('bid/', BidCreateAPIView.as_view(), name='update_bid'),
    path('grade/', GradeCreateAPIView.as_view(), name='update_grade'),

    # Paths to delete an existing vendor on our models
    path('delete/<int:pk>/', VendorDeleteAPIView.as_view(), name='delete'),


]