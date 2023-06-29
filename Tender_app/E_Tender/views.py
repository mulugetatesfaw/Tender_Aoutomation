from datetime import timezone
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from rest_framework import status,generics
from .serializers import BidSerializer,TenderSerializer,VendorSerializer,GradeSerializer,VendorDeleteSerializer
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from .forms import BidForm,TenderForm,VendorForm,GradeForm
from .models import Bid,Tender,Vendor,Grade

# Create your views here.
# create API and function to add vendor 
class VendorCreateAPIView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def post_vender(self, request, *args, **kwargs):    
        form = VendorForm(request.POST)
        if form.is_valid():
            Vendor = form.save()
            serializer = VendorSerializer(Vendor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# An API to add data to our Tender model

class TenderCreateAPIView(generics.CreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def post_tender(self, request, *args, **kwargs):
        form = TenderForm(request.POST)
        if form.is_valid():
            tender = form.save()
            serializer = TenderSerializer(tender)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# Create Bids
class BidCreateAPIView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    form_class = BidForm

    def post_bid(self, request, tender_pk):
        tender = Tender.objects.get(pk=tender_pk)
        if tender.expiry_date and tender.expiry_date < timezone.now():
            return Response({'error': 'Tender expiry date has already passed.'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tender=tender)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
# API to add grades to our bids
class GradeCreateView(generics.CreateAPIView):
    form_class = GradeForm
    serializer_class = GradeSerializer

    def perform_create(self, serializer):
        bid = get_object_or_404(Bid, pk=self.kwargs['pk'])
        serializer.save(bid=bid)
    
# API to update our Vendor model
class VendorUpdateAPIView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def update_vendor(self, request, *args, **kwargs):
        instance = self.get_object()
        form = VendorForm(request.POST, instance=instance)
        if form.is_valid():
            vendor = form.save()
            serializer = VendorSerializer(vendor)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
# API to update our Tendor model
class TenderUpdateAPIView(generics.UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def update_tendor(self, request, *args, **kwargs):
        instance = self.get_object()
        form = TenderForm(request.POST, instance=instance)
        if form.is_valid():
            tender = form.save()
            serializer = TenderSerializer(tender)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# API to update our Bid model
class BidUpdateAPIView(generics.UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def update_bid(self, request, *args, **kwargs):
        instance = self.get_object()
        form = BidForm(request.POST, instance=instance)
        if form.is_valid():
            bid = form.save()
            serializer = BidSerializer(bid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

# API to update our Grade model
class GradeUpdateAPIView(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def update_grade(self, request, *args, **kwargs):
        instance = self.get_object()
        form = GradeForm(request.POST, instance=instance)
        if form.is_valid():
            grade = form.save()
            serializer = GradeSerializer(grade)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
# API to delete specific Vender
class VendorDeleteAPIView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDeleteSerializer

# API to delete specific Tender    
class TenderDeleteView(generics.DestroyAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

# API to delete a specific Bid
class BidDeleteView(generics.DestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

# Api to show available (posted) tenders
class TenderListView(generics.ListAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def get(self, request, format=None):
        tenders = self.get_queryset()
        serializer = self.serializer_class(tenders, many=True)
        return render(request, 'tender_list.html', {'tenders': serializer.data})
    
# Api to show available (posted) bids
class BidListView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get(self, request, format=None):
        bids = self.get_queryset()
        serializer = self.serializer_class(bids, many=True)
        return render(request, 'bid_list.html', {'bids': serializer.data})

