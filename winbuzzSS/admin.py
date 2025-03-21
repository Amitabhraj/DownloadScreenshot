from django.contrib import admin
from winbuzzSS.models import Deposit_Screenshot

# Register your models here.
admin.site.register(Deposit_Screenshot)
# class Deposit_ScreenshotAdmin(admin.ModelAdmin):
#     list_display = ('name', 'deposit_type', 'amount', 'utr', 'trid', 'created_at')
#     search_fields = ('name', 'upi_id', 'utr', 'trid')
#     list_filter = ('deposit_type', 'created_at')