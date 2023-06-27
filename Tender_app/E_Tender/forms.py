#create your forms here
from django import forms
from .models import Bid,Tender,Vendor
#vendor form
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
#Tender form
class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = '__all__'
# Bid form
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'


