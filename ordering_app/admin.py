from django.contrib import admin
from .models import *

admin.site.site_header = "Ordering App Administration"
admin.site.site_title = "Ordering App"

# Register your models here.

@admin.register(Kiosk)
class Kiosk_Admin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class Product_Admin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


@admin.register(AddOn)
class AddOn_Admin(admin.ModelAdmin):
    list_display = ("id", "name", "price")


@admin.register(Selected_Product)
class Selected_Product_Admin(admin.ModelAdmin):
    list_display = ("id", "kiosk", "product", "quantity", "get_add_ons")

    def get_add_ons(self, obj):
        add_ons = obj.add_ons.values_list("name", flat=True).all()
        return ", ".join(add_ons)
    get_add_ons.short_description = "Add-ons"


@admin.register(Order)
class Order_Admin(admin.ModelAdmin):
    list_display = ("id", "queue_number", "kiosk_id", "date_ordered", "status")


@admin.register(Order_Product)
class Order_Product_Admin(admin.ModelAdmin):
    list_display = ("id", "order_id", "product", "quantity", "get_add_ons")

    def get_add_ons(self, obj):
        add_ons = obj.add_ons.values_list("name", flat=True).all()
        return ", ".join(add_ons)
    get_add_ons.short_description = "Add-ons"