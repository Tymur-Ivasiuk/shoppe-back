from django.contrib import admin
from adminsortable2.admin import SortableAdminBase, SortableTabularInline

from .models import *

class PhotoInlines(SortableTabularInline, admin.TabularInline):
    model = Photo
    extra = 0
    fields = ['image_tag', 'image', 'index']
    readonly_fields = ['image_tag']

class AttributeValuesInlines(admin.TabularInline):
    model = AttributeValues
    list_display = ['attribute']
    extra = 0

class ProductAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [
        AttributeValuesInlines,
        PhotoInlines,
    ]


class OrderListInline(admin.TabularInline):
    model = OrderList
    extra = 0

class OrderAdmin(admin.ModelAdmin):

    inlines = [
        OrderListInline
    ]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(Coupon)
admin.site.register(Order, OrderAdmin)

admin.site.register(Profile)
