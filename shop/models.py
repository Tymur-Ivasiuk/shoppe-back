from django.contrib import admin
from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import *
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from .utils import EmailThread
from .validators import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_verify = models.BooleanField(default=False)
    auth_token = models.CharField(max_length=255, unique=True)
    user_json = models.JSONField(null=False, default={}, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    sku = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[validate_positive])
    quantity = models.PositiveIntegerField()
    sale = models.PositiveSmallIntegerField(default=0)
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

    def image_tag(self):
        d = self.photo_set.first()
        return d.image_tag() if d else mark_safe('<p>NONE</p>')
    image_tag.short_description = 'Image'



@receiver(post_save, sender=Product)
def send_email_news(sender, instance, created, **kwargs):
    if instance.is_published:
        emails = EmailNews.objects.all()
        subject = 'New Product'
        message = f'The new {instance.title} is finally available! \n\nhttp://127.0.0.1:8000{instance.get_absolute_url()}'
        recipient_list = [x.email for x in emails]
        EmailThread(subject, message, recipient_list).start()

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
    shipping_price = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_positive], default=0)
    sale = models.ForeignKey('Coupon', on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    payment_method = models.CharField(max_length=255)
    payment_status = models.BooleanField(default=False)

    time_create = models.DateTimeField(auto_now_add=True)

    #address
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postcode = models.PositiveSmallIntegerField()
    town = models.CharField(max_length=255)
    phone = PhoneNumberField()
    email = models.EmailField()

    order_notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('order', kwargs={'order_id': self.id})

class OrderList(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    new_quantity = models.PositiveSmallIntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[validate_positive], default=0)

    @admin.display(description='max count')
    def max_quantity(self):
        return self.product.quantity + self.quantity

    @admin.display(description='image')
    def image_product(self):
        return self.product.photo_set.first().image_tag()

    def __str__(self):
        return str(self.order)


@receiver(post_save, sender=OrderList)
def my_handler2(sender, instance, **kwargs):
    print(OrderList.objects.filter(id=instance.id))
    OrderList.objects.filter(id=instance.id).update(quantity = instance.new_quantity, new_quantity = 0)

@receiver(post_save, sender=OrderList)
def my_handler2(sender, instance, created, **kwargs):
    if created:
        d = Product.objects.get(id=instance.product_id)
        d.quantity -= instance.quantity
        d.save()


@receiver(post_delete, sender=OrderList)
def my_handler3(sender, instance, **kwargs):
    d = Product.objects.get(id=instance.product_id)
    d.quantity += instance.quantity
    d.save()


class Coupon(models.Model):
    code = models.CharField(max_length=25, unique=True)
    sale_percent = models.PositiveSmallIntegerField(validators=[sale_validate])
    max_uses = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.code


class EmailNews(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


class PreViewPhoto(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="img/%Y/%m/%d")
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title

    def get_absolute_url(self):
        return self.product.get_absolute_url()