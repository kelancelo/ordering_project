from django.db import models

# Create your models here.
class Kiosk(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    image_url = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class AddOn(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()

    def __str__(self):
        return self.name


# Many to many relationship between Kiosk and Product.
# This table acts like a Kiosk's shopping cart, it stores the currently
# selected products at a specific Kiosk.
class Selected_Product(models.Model):
    kiosk = models.ForeignKey(Kiosk, on_delete=models.CASCADE, related_name="selected_products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    add_ons = models.ManyToManyField(AddOn)


class Order(models.Model):
    queue_number = models.CharField(max_length=50)
    kiosk = models.ForeignKey(Kiosk, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = [
        ("preparing", "preparing"),
        ("ready to serve", "ready to serve"),
        ("served", "served")
    ]
    status = models.CharField(default="preparing", choices=STATUS_CHOICES, max_length=50)

    def __str__(self):
        return f"{self.id}"


# Many to many relationship between Order and Product.
class Order_Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    add_ons = models.ManyToManyField(AddOn)
