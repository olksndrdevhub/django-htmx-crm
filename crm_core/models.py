from django.db import models

from accounts.models import CrmUser

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    availability = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CrmUser, related_name='products', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('-created_at',)


class Order(models.Model):

    ORDERED = 'ordered'
    DELIVERING = 'delivering'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (DELIVERING, 'Delivering'),
        (COMPLETED, 'Completed'),
    )

    client = models.ForeignKey(CrmUser, related_name='client_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    created_by = models.ForeignKey(CrmUser, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
    
    def get_total(self):
        return sum(int(item.price) for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
