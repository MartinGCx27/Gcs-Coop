from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(transaction_details)
admin.site.register(Price)
admin.site.register(Product)

class PriceInlineAdmin(admin.TabularInline):
    model = Price
    extra = 0


class ProductAdmin(admin.ModelAdmin):
    inlines = [PriceInlineAdmin]
