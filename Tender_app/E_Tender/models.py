from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=255)
    pass_word = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    #compony = models.OneToOneField(Vendor, on_delete=models.CASCADE, related_name='users')

    def str(self):
        return self.user_name
    
class Vendor(models.Model):
    created_by= models.OneToOneField(User, on_delete=models.CASCADE,) # related_name='users')
    phone_number =models.CharField(max_length=20)
    campony = models.CharField(max_length=255)
    TYPE_CHOICES = (
        ('Type 1', 'Construction'),
        ('Type 2', 'Telecomunication'),
        ('Type 3', 'Software products')
    )
    
    catagory = models.CharField(max_length=255, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)

    def str(self):
        return self.created_by

class Tender(models.Model):
    name= models.CharField(max_length=255)
    Description= models.TextField(max_length= 450)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = (
       ('Open', 'Open'),
       ('Closed', 'Closed')
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='open')
    document_path = models.FileField(upload_to='tender_documents/')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,)

    def __str__(self):
        return self.name
    
    def is_expired(self):
        return timezone.now() > self.expiration_date

class Bid(models.Model):
    STATUS_CHOICES = (
        ('winner', 'Win'),
        ('loose', 'Failed'),
        ('pending', 'Pending')
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)#, related_name='bids')
    bid_date = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    document_path = models.FileField(upload_to='bid_documents/')

    def str(self):
        return self.tender

class Grade(models.Model):
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE) #related_name='grade')
    grade_mark = models.CharField(max_length=255)
    collection = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.bid

