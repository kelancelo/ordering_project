from django.urls import path
from . import views

app_name = "ordering_app"
urlpatterns = [
    path("", views.index, name="index"),
    path("add_to_order", views.add_to_order, name="add_to_order"),
    path("selected_products", views.selected_products, name="selected_products"),
    path("checkout", views.checkout, name="checkout"),
    # path("check_order_status", views.check_order_status, name="check_order_status")
]