from datetime import datetime,timezone
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

#import stripe
from .models import User,Vendor,Tender,Bid
from django.core.exceptions import PermissionDenied
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .serializers import VendorSerializer, UserSerializer,TenderSerializer,BidSerializer
#from rest_framework.authtoken.views import ObtainAuthToken
#from rest_framework.authtoken.models import Token
#stripe.api_key = 'your_stripe_secret_key'
# Create your views here.
# Home page

#authentication
""" class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'user_id': token.user_id})

obtain_auth_token = CustomObtainAuthToken.as_view()
 """

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# create venders after authentication
class CreateVendorView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def create_vender(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            data = response.data
            data['user'] = request.user.id
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return response
        
# retrieve all venders
class VendorListView(generics.ListAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

class VendorDetailView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

class VendorUpdateView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.vendor

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({'message': 'Vendor updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return response

class VendorDeleteView(generics.DestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.vendor

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({'message': 'Vendor deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return response
        
# create tenders for bid
class TenderCreateView(generics.CreateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def create_tender(self, request, *args, **kwargs):
        vendor = request.user.vendor
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(vendor=vendor)
        return Response({'message': 'Tender created successfully.'}, status=status.HTTP_201_CREATED)

# retrieve tenders
class TenderListView(generics.ListAPIView):
    serializer_class = TenderSerializer

    def get_queryset(self):
        now = timezone.now()
        open_tenders = Tender.objects.filter(expiration_date__gt=now)
        closed_tenders = Tender.objects.filter(expiration_date__lte=now)
        open_tenders.update(status='Open')
        closed_tenders.update(status='Closed')
        return open_tenders

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    #permission_classes = [permissions.IsAuthenticated]

class TenderDetailView(generics.RetrieveAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    #permission_classes = [permissions.IsAuthenticated]

class TenderUpdateView(generics.UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        tender = super().get_object()
        vendor = self.request.user.vendor
        if tender.vendor != vendor:
            raise PermissionDenied("You don't have permission to update this Tender.")
        return tender

    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response({'message': 'Tender updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return response

class TenderDeleteView(generics.DestroyAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        tender = super().get_object()
        vendor = self.request.user.vendor
        if tender.vendor != vendor:
            raise PermissionDenied("You don't have permission to delete this Tender.")
        return tender

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return Response({'message': 'Tender deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return response
        
#Bid processing using strip payment method

class BidCreateView(generics.CreateAPIView):
    serializer_class = BidSerializer

    def post(self, request, *args, **kwargs):
        tender_id = kwargs.get('tender_id')
        try:
            tender = Tender.objects.get(id=tender_id)
        except Tender.DoesNotExist:
            return Response({'message': 'Tender does not exist'}, status=status.HTTP_404_NOT_FOUND)

        if datetime.now().date() > tender.expiration_date:
            return Response({'message': 'Tender has expired'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(tender=tender, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#retrive bids
class BidListView(generics.ListAPIView):
    serializer_class = BidSerializer

    def get_queryset(self):
        tender = Tender.objects.get(pk=self.kwargs['pk'])
        bids = Bid.objects.filter(tender=tender).order_by('-amount')

        # get the expiry date of the tender
        expiry_date = tender.expiration_date

        # loop through all the bids and update their status based on the amount and expiry date
        for bid in bids:
            if bid.amount >= bids.first().amount and expiry_date <= timezone.now():
                bid.status = 'winner'
            elif expiry_date > timezone.now():
                bid.status = 'pending'
            else:
                bid.status = 'loose'
            bid.save()

        return bids

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





""" class BidCreateView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create_bid(self, request, *args, **kwargs):
        tender = Tender.objects.get(pk=kwargs['pk'])
        service_fee = tender.service_fee
        expiration_date = tender.expiration_date
        vendor = request.user.vendor

        if not stripe.Customer.list(email=vendor.email)['data']:
            customer = stripe.Customer.create(email=vendor.email, source=request.data['stripeToken'])
            vendor.stripe_customer_id = customer.id
            vendor.save()
        else:
            customer = stripe.Customer.list(email=vendor.email)['data'][0]

        if customer.default_source is None:
            return Response({'message': 'No payment method found.'}, status=status.HTTP_400_BAD_REQUEST)

        if expiration_date < timezone.now().date():
            return JsonResponse({'message': 'The expiration date for this Tender has passed.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            charge = stripe.Charge.create(
                amount=service_fee,
                currency='usd',
                customer=customer.id,
                description=f'Service fee for Tender {tender.pk}'
            )
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            return Response({'message': err.get('message')}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(vendor=vendor, tender=tender)
        return JsonResponse({'message': 'Bid submitted successfully.'}, status=status.HTTP_201_CREATED)

    def post(self, request, *args, **kwargs):
        return self.create_bid(request, *args, **kwargs)
 """