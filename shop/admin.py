from django.contrib import admin
from adminsortable2.admin import SortableAdminBase, SortableTabularInline
from django.forms import Widget
from django.forms.utils import flatatt
from django.utils.html import format_html

from .models import *
from .forms import *

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

class OrderListTabularFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        print(dir(self))
        for i in self.forms:
            print(i.cleaned_data)
            if i.cleaned_data['new_quantity']:
                print(i.cleaned_data['product'].quantity)
                if i.cleaned_data['new_quantity'] <= i.cleaned_data['product'].quantity:
                    d = i.cleaned_data['product']
                    order_list_item = OrderList.objects.get(order=i.cleaned_data['order'], product=i.cleaned_data['product'])
                    if i.cleaned_data['quantity']:
                        d.quantity -= i.cleaned_data['new_quantity'] - i.cleaned_data['quantity']
                    else:
                        d.quantity -= i.cleaned_data['new_quantity']

                    d.save()
                    order_list_item.quantity = i.cleaned_data['new_quantity']
                    order_list_item.save()
                    print(i.cleaned_data['product'].quantity)
                else:
                    raise forms.ValidationError("Dates are incorrect")



class OrderListInline(admin.TabularInline):
    formset = OrderListTabularFormset
    form = OrderListFormAdmin
    model = OrderList
    extra = 0
    readonly_fields = ('price',)

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
