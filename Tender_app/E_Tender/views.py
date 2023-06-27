from django.shortcuts import render, redirect
from rest_framework import status,generics
from .serializers import BidSerializer,TenderSerializer,VendorSerializer,GradeSerializer
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from .forms import BidForm,TenderForm,VendorForm,GradeForm
from .models import Bid,Tender,Vendor,Grade

# Create your views here.
# create function to add vendor 
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

# An API to add data to our Bid model

class BidCreateAPIView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def post_bid(self, request, *args, **kwargs):
        form = BidForm(request.POST)
        if form.is_valid():
            bid = form.save()
            serializer = BidSerializer(bid)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
# API to grade our bid
class GradeCreateAPIView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

    def post_grade(self, request, *args, **kwargs):
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save()
            serializer = BidSerializer(grade)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
