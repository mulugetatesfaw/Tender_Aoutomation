#create your forms here
from django import forms
from .models import Bid,Tender

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'
class TenderForm(forms.ModelForm):
    class Meta:
        model = Tender
        fields = '__all__'
