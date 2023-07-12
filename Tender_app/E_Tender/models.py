from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    
class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL, null=True, blank=True) # related_name='users')
    phone_number =models.CharField(max_length=20)
    campony = models.CharField(max_length=255,null=True)
    TYPE_CHOICES = (
        ('Construction', 'Construction'),
        ('Telecomunication', 'Telecomunication'),
        ('Software products', 'Software products')
    )
    
    catagory = models.CharField(max_length=255, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.campony

class Tender(models.Model):
    tittle= models.CharField(max_length=255)
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
    legalized_documents = models.FileField(upload_to='legalized_documents/')
    #vendors = models.ManyToManyField(Vendor,on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.tittle
    

class Bid(models.Model):
    STATUS_CHOICES = (
        ('winner', 'Winner'),
        ('loose', 'Failed'),
        ('pending', 'Pending')
    )

    #vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    tender = models.ForeignKey(Tender, on_delete=models.SET_NULL, null=True)#, related_name='bids')
    bid_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_id')
    status = models.CharField(max_length=255, choices=STATUS_CHOICES,null=True, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    document_path = models.FileField(upload_to='bid_documents/')

    def __str__(self):
        return f'Bid of {self.amount} by {self.user.username} for Tender {self.tender.id}'



