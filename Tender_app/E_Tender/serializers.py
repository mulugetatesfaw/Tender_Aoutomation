from rest_framework import serializers
from .models import Bid,Tender,Vendor

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model =Vendor
        fields = 'all'

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = 'all'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = 'all'
