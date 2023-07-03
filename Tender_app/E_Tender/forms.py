#create your forms here
from django import forms
from .models import Bid,Tender,Vendor,Grade

__all__ = [
    'PaymentForm',
    'BidForm',
]
class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=[('usd', 'USD'),('etb', 'ETB'), ('eur', 'EUR')])
    description = forms.CharField(max_length=255)
    stripe_customer_id = forms.CharField(max_length=255)

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = '__all__'

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

    def __init__(self, vendor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Tender Name'
        self.fields['Description'].label = 'Tender Description'
        self.fields['created_at'].label = 'Tender Creation Date'
        self.fields['expiration_date'].label = 'Tender Expiration Date'
        self.fields['service_fee'].label = 'Service Fee'
        self.fields['status'].label = 'Tender Status'
        self.fields['document_path'].label = 'Document Path'
        self.fields['vendor'].widget = forms.HiddenInput()
        self.vendor = vendor

    def save(self, commit=True):
        tender = super().save(commit=False)
        tender.vendor = self.vendor
        if commit:
            tender.save()
        return tender

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
