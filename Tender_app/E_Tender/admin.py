from django.contrib import admin
from.import models

# Register your models here.
admin.site.site_header='E-Tender Administrator'
admin.site.site_title='Tender Aoutomation System'
admin.site.index_title='Well come to E-Tender'

@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display=[ 'bid_date', 'status']
    search_fields=[' status', 'bid_date']
    list_filter = ['bid_date']
    search_fields=[' status', 'bid_date']

@admin.register(models.Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display=['status']
    search_fields=['post_date', 'expiry_date','status']
    list_filter = ['status']
    search_fields=['post_date', 'expiry_date','status']

@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display=[ 'user', 'campony']
    search_fields=['user', 'campony']
    list_filter = ['user', 'campony']
    search_fields=['user' ,'campony']
