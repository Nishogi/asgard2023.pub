from django.contrib import admin
from .models import Order
from import_export.admin import ImportExportMixin


class OrderAdmin(ImportExportMixin, admin.ModelAdmin):
    fieldsets = [
        ("Menu", {"fields": ["menu"]}),
        ("prénom", {"fields": ["firstName"]}),
        ("nom", {"fields": ["lastName"]}),
        ("boisson", {"fields": ["drinks"]}),
        ("adress", {"fields": ["address"]}),
        ("time", {"fields": ["deliveryTime"]}),
        ("commentaires", {"fields": ["comments"]}),
    ]
    list_display = (
        "menu",
        "firstName",
        "lastName",
        "drinks",
        "address",
        "deliveryTime",
        "comments",
    )
    list_filter = ["menu", "deliveryTime"]


admin.site.register(Order, OrderAdmin)
