from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    category = models.CharField(max_length=255)

    def str(self):
        return self.name

class User(models.Model):
    user_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    company = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='users')

    def str(self):
        return self.user_name

class Tender(models.Model):
    TYPE_CHOICES = (
        ('Type 1', 'construction'),
        ('Type 2', 'Telecomunication'),
        ('Type 3', 'Software products')
    )

    type = models.CharField(max_length=255, choices=TYPE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    document_path = models.FileField(upload_to='tender_documents/')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='tenders')

    def str(self):
        return f'Tender {self.id} ({self.type})'

class Bid(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    )

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name='bids')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='Pending')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    document_path = models.FileField(upload_to='bid_documents/')

    def str(self):
        return f'Bid {self.id} by {self.vendor.name}'

class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.OneToOneField(Bid, on_delete=models.CASCADE, related_name='grade')
    result = models.CharField(max_length=255)
    collection = models.CharField(max_length=255)
    date = models.DateField()

    def str(self):
        return f'Grade for Bid {self.bid.id} by {self.user.user_name}'
