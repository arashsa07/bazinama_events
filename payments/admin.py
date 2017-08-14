from django.contrib import admin

from .models import Payment, Gateway


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'paid_status', 'gateway', 'created_time')
    list_filter = ('paid_status', 'gateway')

admin.site.register(Gateway)
admin.site.register(Payment, PaymentAdmin)