from django.shortcuts import render
from .models import *
import uuid
import platform
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

# Create your views here.
def index(request):
    return render(request, "ordering_app/index.html", {
        "products": Product.objects.all(),
        "add_ons": AddOn.objects.all()
    })


# Helper function for getting the kiosk object from the DB.
def get_kiosk(mac):
    kiosk = None
    # Check if the Kiosk exists in the DB.
    try:
        kiosk = Kiosk.objects.get(id=mac)
    # If not, add the Kiosk in the DB.
    except Kiosk.DoesNotExist:
        # platform.uname().node gets the machine's name
        kiosk = Kiosk.objects.create(id=mac, name=platform.uname().node)
    return kiosk


def add_to_order(request):
    # Get form data.
    product = Product.objects.get(id=request.POST["product_id"])
    quantity = int(request.POST["quantity"])
    add_on_ids = request.POST.getlist("add_on_id")
    # Get Kiosk's MAC address (used as PK for the Kiosk).
    mac = str(uuid.getnode())
    kiosk = get_kiosk(mac)
    # Add the product to the Kiosk's "shopping cart".
    selected_product = Selected_Product.objects.create(kiosk=kiosk, product=product, quantity=quantity)
    # Add the add-ons to the product.
    for id in add_on_ids:
        add_on = AddOn.objects.get(id=id)
        selected_product.add_ons.add(add_on)
    messages.add_message(request, messages.SUCCESS, "Product added to order!")
    return HttpResponseRedirect(reverse("ordering_app:index"))


def selected_products(request):
    mac = str(uuid.getnode())
    kiosk = get_kiosk(mac)
    selected_products = kiosk.selected_products.all()
    total_items = total_price = 0
    # For each selected product, add its quantity to the total_items,
    # compute its product total then add the product total to the total_price.
    for sp in selected_products:
        total_items += sp.quantity
        product_total = 0
        product_total += sp.quantity * sp.product.price
        for add_on in sp.add_ons.all():
            product_total += add_on.price * sp.quantity
        total_price += product_total
        sp.product_total = product_total
    return render(request, "ordering_app/selected_products.html", {
        "selected_products": selected_products,
        "total_items": total_items,
        "total_price": total_price
    })
    

def checkout(request):
    kiosk = Kiosk.objects.get(id=str(uuid.getnode()))
    selected_products = kiosk.selected_products.all()
    # If selected_products is empty, redirect to the index page.
    if len(selected_products) == 0:
        return HttpResponseRedirect(reverse("ordering_app:index"))
    now = datetime.datetime.now()
    # I generated the queue number by concatenating the current time's minute,
    # second and first 2 digits of the microsecond.
    queue_number = f"{now.minute}{now.second}{str(now.microsecond)[:2]}"
    order = Order.objects.create(queue_number=queue_number, kiosk=kiosk)
    # This loop is similar to the one in selected_products view function with the addition
    # of adding each selected product to the order then deleting it.
    total_items = total_price = 0
    order_products = []
    for sp in selected_products:
        total_items += sp.quantity
        product_total = 0
        product_total += sp.quantity * sp.product.price
        order_product = Order_Product.objects.create(order=order, product=sp.product, quantity=sp.quantity)
        for add_on in sp.add_ons.all():
            product_total += add_on.price * sp.quantity
            order_product.add_ons.add(add_on)
        total_price += product_total
        order_product.product_total = product_total
        order_products.append(order_product)
        sp.delete()
    messages.add_message(request, messages.SUCCESS, "Checkout success!")
    return render(request, "ordering_app/checkout_done.html", {
        "order": order,
        "order_products": order_products,
        "total_items": total_items,
        "total_price": total_price
    })
    

# def check_order_status(request):
#     return render(request, "ordering_app/check_order_status.html")