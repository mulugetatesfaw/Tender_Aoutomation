from django.urls import path
from .views import VendorCreateAPIView,TenderCreateAPIView,GradeCreateAPIView,GradeUpdateAPIView,VendorDeleteAPIView,TenderDeleteAPIView,BidDeleteAPIView,TenderListAPIView,BidListAPIView,VendorDetailAPIView,VendorUpdateAPIView,TenderUpdateAPIView
from .import views
from.views import home
app_name = 'E_Tender'

urlpatterns = [
    # Paths to create  models
    path('', home, name='home'),
    path('vendor/create/', VendorCreateAPIView.as_view(), name='vendor_create'),
    path('vendor/<int:pk>/', VendorDetailAPIView.as_view(), name='vendor_detail'),
    path('vendor/<int:pk>/update/', VendorUpdateAPIView.as_view(), name='vendor_update'),
    path('vender/<int:pk>/delete/', VendorDeleteAPIView.as_view(), name='vender-delete'),

    path('tenders/create/', TenderCreateAPIView.as_view(), name='tender_create'),
    path('tenders/', TenderListAPIView.as_view(), name='tender-list'),
    path('tenders/<int:pk>/update/', TenderUpdateAPIView.as_view(), name='tender_update'),
    path('tenders/<int:pk>/delete/', TenderDeleteAPIView.as_view(), name='tender_delete'),

    path('<int:tender_id>/payment/',views.create_payment_intent, name='create_payment_intent'),
    path('<int:tender_id>/bid/', views.submit_bid, name='submit_bid'),
    path('bids/', BidListAPIView.as_view(), name='bid-list'),
    path('bid/<int:pk>/delete/', BidDeleteAPIView.as_view(), name='bid-delete'),
    
    
    path('bid/<int:pk>/grade/create/', GradeCreateAPIView.as_view(), name='create-grade'),
    path('grades/<int:pk>/update/', GradeUpdateAPIView.as_view(), name='grade_update'),
    ]


