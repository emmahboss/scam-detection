from django.contrib import admin
from .models import User, Address, CreditCard

class fraudDetectionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(User)
admin.site.register(Address)
admin.site.register(CreditCard)
