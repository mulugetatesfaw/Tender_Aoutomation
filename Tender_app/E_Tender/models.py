from django.db import models
from django.contrib.auth.models import User
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
    vender_of= models.OneToOneField(User, on_delete=models.CASCADE,) # related_name='users')
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
        return self.vender_of

class Tender(models.Model):
    post_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
       ('Open', 'Open'),
       ('Closed', 'Closed')
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='open')
    document_path = models.FileField(upload_to='tender_documents/')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,)# related_name='tenders')

    def str(self):
        return self.Vendor

class Bid(models.Model):
    STATUS_CHOICES = (
        ('winner', 'Win'),
        ('loose', 'Failed'),
        ('pending', 'Pending')
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)#, related_name='bids')
    bid_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    document_path = models.FileField(upload_to='bid_documents/')

    def str(self):
        return self.tender

class Grade(models.Model):
    graded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE) #related_name='grade')
    grade_mark = models.CharField(max_length=255)
    collection = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.bid

