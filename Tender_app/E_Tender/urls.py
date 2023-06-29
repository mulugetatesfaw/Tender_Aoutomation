from django.urls import path
from .views import BidCreateAPIView,VendorCreateAPIView,TenderCreateAPIView,GradeCreateAPIView,VendorDeleteAPIView,delete_tender,delete_bid,TenderList,BidList
app_name = 'E_Tender'

urlpatterns = [
    # Paths to create models
    path('vendor/', VendorCreateAPIView.as_view(), name='post_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='post_tender'),
    path('tenders/<int:tender_pk>/bids/', BidCreateAPIView.as_view(), name='bid-create'),
    path('grade/', GradeCreateAPIView.as_view(), name='post_grade'),
    
    # Paths to update an existing data on our models
    path('vendor/', VendorCreateAPIView.as_view(), name='update_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='update_tender'),
    path('bid/', BidCreateAPIView.as_view(), name='update_bid'),
    path('grade/', GradeCreateAPIView.as_view(), name='update_grade'),

    # Paths to delete an existing data on our models
    path('delete/<int:pk>/', VendorDeleteAPIView.as_view(), name='delete'),
    path('tenders/<int:pk>/', delete_tender, name='delete_tender'),
    path('bids/<int:pk>/', delete_bid, name='delete_bid'),
     # path to populate bids and tenders 
    path('tenders/', TenderList.as_view(), name='tender-list'),
    path('bids/', BidList.as_view(), name='bid-list'),
    ]


