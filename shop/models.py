from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from phone_field import PhoneField

from .validators import *


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_positive])
    quantity = models.PositiveIntegerField()
    # in_stock = models.BooleanField(default=0)
    description = models.TextField(blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, default='0')

    #m2m fields
    attribute_SET = models.ManyToManyField(
        'Attribute',
        through='AttributeValues',
        through_fields=('product', 'attribute'),
    )

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_page', kwargs={'product_id': self.id})

class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class AttributeValues(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    value_text = models.CharField(max_length=128, default=' ')


class Photo(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    image = models.ImageField(upload_to="img/%Y/%m/%d")
    index = models.PositiveSmallIntegerField(default=0, blank=False, null=False, db_index=True)

    class Meta:
        ordering = ['index']

    def image_tag(self):
        return mark_safe('<img src="%s" height="100" />' % (self.image.url))
    image_tag.short_description = 'Image'


class Review(models.Model):
    text = models.TextField(max_length=255)
    star_rating = models.PositiveSmallIntegerField(validators=[starValid], default=1)
    name = models.CharField(max_length=255, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, null=True)

    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)

class Order(models.Model):
    status_var = [
        ('New', 'New'),
        ('In processing', 'In processing'),
        ('Confirmed', 'Confirmed'),
        ('Delivered', 'Delivered'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    status = models.CharField(max_length=255, choices=status_var, default='New')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    #address
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.PositiveSmallIntegerField()
    town = models.CharField(max_length=255)
    phone = PhoneField()
    email = models.EmailField()

    order_notes = models.TextField(blank=True)

    def __str__(self):
        return self.id

class OrderList(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
