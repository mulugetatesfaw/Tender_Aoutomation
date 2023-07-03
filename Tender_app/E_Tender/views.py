#from datetime import timezone
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework import status,generics,permissions
from .serializers import BidSerializer,TenderSerializer,VendorSerializer,GradeSerializer,VendorDeleteSerializer
from rest_framework.response import Response
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from .forms import PaymentForm
from .forms import BidForm,TenderForm,VendorForm,GradeForm
from .models import Bid,Tender,Vendor,Grade

# Create your views here.
# Home page
def home(request):
    return render(request, 'home.html')
# create API and function to add vendor 
class VendorCreateAPIView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    template_name = 'vendor_create.html'

    def get_success_url(self):
        return reverse('vendor_create.html')

    def post(self, request, *args, **kwargs):
        form = VendorForm(request.POST)
        if form.is_valid():
            vendor = form.save()
            serializer = VendorSerializer(vendor)
            return render(request, self.template_name, {'success_url': self.get_success_url()})
        return render(request, self.template_name, {'form': form})


class VendorDetailAPIView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    template_name = 'vendor_detail.html'

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        return render(request, self.template_name, {'vendor': vendor})

# API to update our Vendor model
class VendorUpdateAPIView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def put(self, request, pk):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API to delete specific Vender
class VendorDeleteAPIView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDeleteSerializer


# An API to add data to our Tender model

class TenderCreateAPIView(generics.CreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        form = TenderForm(vendor=request.user.vendor)
        return render(request, 'tender_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TenderForm(vendor=request.user.vendor, data=request.POST, files=request.FILES)
        if form.is_valid():
            tender = form.save()
            return render(request, 'tender_created.html', {'tender': tender})
        return render(request, 'tender_create.html', {'form': form})
    
# Set up Stripe API key
#stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(['GET', 'POST'])
def create_payment_intent(request, tender_id):
    """
    View function to render the payment form and create a payment intent
    """
    # Retrieve Tender object
    tender = get_object_or_404(Tender, id=tender_id)

    if request.method == 'POST':
        # Process payment form
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Calculate service fee
            service_fee = tender.service_fee

            # Calculate total amount
            total_amount = service_fee + form.cleaned_data['amount']

            # Create payment intent
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency=form.cleaned_data['currency'],
                description=form.cleaned_data['description'],
                metadata={'stripe_customer_id': form.cleaned_data['stripe_customer_id']}
            )

            # Render payment confirmation template
            return render(request, 'payment_confirmation.html', {'client_secret': payment_intent.client_secret})

    else:
        # Render payment form template
        form = PaymentForm()
        return render(request, 'payment_form.html', {'tender': tender, 'form': form})

@api_view(['POST'])
def submit_bid(request, tender_id):
    """
    API endpoint to submit a Bid for a Tender
    """
    # Retrieve Tender object
    tender = get_object_or_404(Tender, id=tender_id)

    # Check if Tender is unexpired
    if tender.is_expired():
        return Response({'error': 'This Tender has expired.'}, status=400)

    # Process Bid form
    serializer = BidSerializer(data=request.data)
    if serializer.is_valid():
        # Create Bid object
        bid = serializer.save(tender=tender, bidder=request.user)

        # Render Bid submission confirmation template
        return render(request, 'bid_confirmation.html', {'bid': bid})
# API to update our Tendor model
class TenderUpdateAPIView(generics.UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    form_class = TenderForm
    template_name = 'tender_update.html'

    def get_success_url(self):
        return reverse('tender_update', kwargs={'pk': self.get_object().pk})

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(instance=instance)
        return render(request, self.template_name, {'form': form, 'tender': instance})

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return render(request, self.template_name, {'form': form, 'tender': instance})
    
# API to delete specific Tender    
class TenderDeleteAPIView(generics.DestroyAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    template_name = 'tender_confirm_delete.html'

    def get_success_url(self):
        return reverse('tender_list')

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        return render(request, self.template_name, {'tender': instance})

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# API to add grades to our bids
class GradeCreateAPIView(generics.CreateAPIView):
    form_class = GradeForm
    serializer_class = GradeSerializer
    template_name = 'my_template.html'
 # In the example above, my_page_name is the name of the URL pattern 
 # that corresponds to the HTML page you want to redirect
    def get_success_url(self):
        return reverse('my_page_name')

    def perform_create(self, serializer):
        bid = get_object_or_404(Bid, pk=self.kwargs['pk'])
        serializer.save(bid=bid)
        return render(self.request, self.template_name, {'success_url': self.get_success_url()})

    

""" # API to update our Bid model
class BidUpdateAPIView(generics.UpdateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def update_bid(self, request, *args, **kwargs):
        instance = self.get_object()
        form = BidForm(request.POST, instance=instance)
        if form.is_valid():
            bid = form.save()
            serializer = BidSerializer(bid)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST) """

# API to update our Grade model
class GradeUpdateAPIView(generics.UpdateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    form_class = GradeForm
    template_name = 'grade_update.html'

    def get_success_url(self):
        return reverse('grade_update', kwargs={'pk': self.get_object().pk})

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(instance=instance)
        return render(request, self.template_name, {'form': form, 'grade': instance})

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        form = self.form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return render(request, self.template_name, {'form': form, 'grade': instance})



# API to delete a specific Bid
class BidDeleteAPIView(generics.DestroyAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

#view tender detail
class TenderListAPIView(generics.ListAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer

    def get(self, request, format=None):
        tenders = self.get_queryset()
        serializer = self.serializer_class(tenders, many=True)
        return render(request, 'tender_list.html', {'tenders': serializer.data})
    
# Api to show available (posted) bids
class BidListAPIView(generics.ListAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer

    def get(self, request, format=None):
        bids = self.get_queryset()
        serializer = self.serializer_class(bids, many=True)
        return render(request, 'bid_list.html', {'bids': serializer.data})

