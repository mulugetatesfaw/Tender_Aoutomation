from django.shortcuts import render, redirect
from rest_framework import status,generics
from .serializers import BidSerializer
from rest_framework.response import Response
#from rest_framework.decorators import api_view
from .forms import BidForm
from .models import Bid,Vendor,Tender,Grade,User

# Create your views here.
# An API to add data to our Vendor model

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
