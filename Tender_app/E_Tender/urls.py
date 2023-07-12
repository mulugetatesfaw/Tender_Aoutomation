from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    #obtain_auth_token,
    CreateUserView,

    CreateVendorView,
    VendorListView,
    VendorDetailView,
    VendorUpdateView,
    VendorDeleteView,
    TenderCreateView,
    TenderDetailView,
    TenderListView,
    TenderUpdateView,
    TenderDeleteView,
    BidCreateView,
    BidListView,

)
app_name = 'E_Tender'

urlpatterns = [
    # user authentication
    path('users/', CreateUserView.as_view(), name='create_user'),

    # vendors operation path
    path('vendors/create', CreateVendorView.as_view(), name='create_vendor'),
    path('vendors/<int:pk>/', VendorDetailView.as_view(), name='vendor_detail'),
    path('vendors/all/', VendorListView.as_view(), name='vendor_list'),
    path('vendors/update/', VendorUpdateView.as_view(), name='vendor_update'),
    path('vendors/delete/', VendorDeleteView.as_view(), name='vendor_delete'),
   
   # tenders opration
    path('tenders/create/', TenderCreateView.as_view(), name='tender_create'),
    path('tenders/<int:pk>/', TenderDetailView.as_view(), name='tender_detail'),
    path('tenders/all/', TenderListView.as_view(), name='tender_list'),
    path('tenders/<int:pk>/update/', TenderUpdateView.as_view(), name='tender_update'),
    path('tenders/<int:pk>/delete/', TenderDeleteView.as_view(), name='tender_delete'),

# Bid processing
 path('tender/<int:pk>/bid/', BidCreateView.as_view(), name='bid_create'),
 path('tender/<int:pk>/bids/', BidListView.as_view(), name='bid_list'),
]

