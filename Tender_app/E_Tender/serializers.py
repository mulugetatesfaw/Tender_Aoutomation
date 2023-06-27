from rest_framework import serializers
from .models import Bid,Tender

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = 'all'
class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = 'all'
