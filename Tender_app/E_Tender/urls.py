from django.urls import path
from .views import BidCreateAPIView,VendorCreateAPIView,TenderCreateAPIView,GradeCreateView,VendorDeleteAPIView,TenderDeleteView,BidDeleteView,TenderListView,BidListView
app_name = 'E_Tender'

urlpatterns = [
    # Paths to create  models
    path('vendor/', VendorCreateAPIView.as_view(), name='post_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='post_tender'),
    path('tender/<int:tender_pk>/bids/', BidCreateAPIView.as_view(), name='bid-create'),
    path('bid/<int:pk>/grade/create/', GradeCreateView.as_view(), name='create-grade'),
    
    # Paths to update an existing data on our models
    path('vendor/', VendorCreateAPIView.as_view(), name='update_vendor'),
    path('tender/', TenderCreateAPIView.as_view(), name='update_tender'),
    path('bid/', BidCreateAPIView.as_view(), name='update_bid'),
    path('grade/', GradeCreateView.as_view(), name='update_grade'),

    # Paths to delete an existing data on our models
    path('vender/<int:pk>/delete/', VendorDeleteAPIView.as_view(), name='vender-delete'),
    path('tender/<int:pk>/delete/', TenderDeleteView.as_view(), name='tender-delete'),
    path('bid/<int:pk>/delete/', BidDeleteView.as_view(), name='bid-delete'),

     # path to populated bids and tenders 
    path('tenders/', TenderListView.as_view(), name='tender-list'),
    path('bids/', BidListView.as_view(), name='bid-list'),
    ]


