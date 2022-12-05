from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    description = models.TextField(blank=True)
    category_id = models.ForeignKey('Category', on_delete=models.PROTECT, default='0')

    #m2m fields
    attribute_SET = models.ManyToManyField(
        'Attribute',
        through='AttributeValues',
        through_fields=('product_id', 'attribute_id')
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
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    attribute_id = models.ForeignKey('Attribute', on_delete=models.CASCADE)

    value_text = models.CharField(max_length=128, default=' ')


class Photo(models.Model):
    product_id = models.ForeignKey('Product', on_delete=models.PROTECT)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    index = models.PositiveSmallIntegerField(default=0, blank=False, null=False, db_index=True)

    class Meta:
        ordering = ['index']

    def image_tag(self):
        return mark_safe('<img src="%s" height="100" />' % (self.image.url))
    image_tag.short_description = 'Image'

