#create your forms here
from django import forms
from .models import Bid,Tender,Vendor,Grade

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

# Grade bid form
class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'

#form to delete specific Vender
class VendorDeleteForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = []
        
# Delete tender form
class TenderDeleteForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = []
#Form to delete bid
class BidDeleteForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = []
