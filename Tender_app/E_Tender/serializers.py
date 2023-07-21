from rest_framework import serializers
from django.contrib.auth.models import User
from .models import User,Bid,Tender,Vendor
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

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