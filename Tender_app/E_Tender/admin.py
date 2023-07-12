from django.contrib import admin
from.import models

# Register your models here.
admin.site.site_header='E-Tender Administrator'
admin.site.site_title='Tender Aoutomation System'
admin.site.index_title='Well come to E-Tender'

@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    list_display=['bid_date','amount', 'status',]
    search_fields=['bid_date','amount','status']
    list_filter = ['bid_date','amount', 'status']
    search_fields=['bid_date', 'amount','status']

@admin.register(models.Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display=['tittle','created_at','expiration_date','service_fee','status']
    search_fields=['tittle','created_at','expiration_date','service_fee','status']
    list_filter = ['tittle','created_at','expiration_date','service_fee','status']
    search_fields=['tittle','created_at','expiration_date','service_fee','status']

@admin.register(models.Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display=['user', 'phone_number','address','campony','catagory']
    search_fields=['user', 'phone_number','address','campony','catagory']
    list_filter = ['user', 'phone_number','address','campony','catagory']
    search_fields=['user', 'phone_number','address','campony','catagory']
