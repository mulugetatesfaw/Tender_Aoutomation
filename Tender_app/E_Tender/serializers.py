from rest_framework import serializers
from .models import User,Bid,Tender,Vendor

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model =Vendor
        fields = '__all__'

class TenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tender
        fields = '__all__'

class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'
        
#serialiser to delete specific vendor
class VendorDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = []