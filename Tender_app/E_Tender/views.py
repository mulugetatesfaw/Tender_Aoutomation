from datetime import datetime,timezone
from rest_framework.response import Response
from rest_framework import status


#import stripe
from .models import Vendor,Tender,Bid
from django.core.exceptions import PermissionDenied
from rest_framework import generics, status, permissions
from .serializers import VendorSerializer,UserSerializer,TenderSerializer,BidSerializer
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import get_user_model

#registration 
User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully"
        }, status=status.HTTP_201_CREATED)

class AuthenticationView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
    
# create venders after authentication
class CreateVendorView(generics.CreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [permissions.IsAuthenticated]

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
    

class VendorDetailView(generics.RetrieveAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class VendorUpdateView(generics.UpdateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    

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
    

class TenderDetailView(generics.RetrieveAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    

class TenderUpdateView(generics.UpdateAPIView):
    queryset = Tender.objects.all()
    serializer_class = TenderSerializer
    
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
        
#Bid processing 

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




