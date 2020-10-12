from django.contrib import admin
from .models import Account, Customer, VPS, SMSCustomer, CorrlinksToSMS, SMSToCorrlinks, APIKey, Image
import admin_thumbnails


# Register your models here.
class AccountAdmin(admin.TabularInline):
    # list_display = ('email', 'status', 'VPS')
    model = Account


class AccountAdmin2(admin.ModelAdmin):
    list_display = ('email', 'status', 'VPS')
    list_filter = ('email', 'status', 'VPS')


class VPSAdmin(admin.ModelAdmin):
    list_display = ('VPS_Name', 'notes', 'active', 'disabled')
    inlines = [AccountAdmin]

    def active(self, obj):
        return obj.get_active_count()

    def disabled(self, obj):
        return obj.get_disabled_count()


class CorrlinksToSMSAdmin(admin.ModelAdmin):
    list_display = ('createdAt', '_from', 'to', 'status')
    list_filter = ('createdAt', 'status', 'to', '_from')


@admin_thumbnails.thumbnail('image')
class ImageAdmin(admin.TabularInline):
    model = Image


class SMSToCorrlinksAdmin(admin.ModelAdmin):
    list_display = ('createdAt', 'id', 'Images_Count', '_from', 'status')
    list_filter = ('createdAt', 'status', '_from')

    inlines = [ImageAdmin]

    def Images_Count(self, obj):
        return obj.get_image_count()


class SMSCustomerAdmin(admin.TabularInline):
    # list_display = ('co rrlinks_Customer', 'name', 'phone_Number')
    model = SMSCustomer


class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'due_Date', 'status', 'Images_Count', 'balance', 'phone_Number', 'corrlinks_ID', 'corrlinks_Account')
    inlines = [SMSCustomerAdmin, ImageAdmin]
    list_filter = ('due_Date', 'status', 'corrlinks_Account')

    def Images_Count(self, obj):
        return obj.get_image_count_customer()


admin.site.register(Account, AccountAdmin2)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(VPS, VPSAdmin)

# admin.site.register(SMSCustomer, SMSCustomerAdmin)

admin.site.register(SMSToCorrlinks, SMSToCorrlinksAdmin)
admin.site.register(CorrlinksToSMS, CorrlinksToSMSAdmin)
admin.site.register(APIKey)
