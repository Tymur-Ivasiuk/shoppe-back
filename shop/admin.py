from adminsortable2.admin import SortableAdminBase, SortableTabularInline

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
    search_fields = ['title', 'sku']
    list_display = ['title', 'price', 'quantity', 'sku']
    list_editable = ['price']

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
                if i.cleaned_data['new_quantity'] - i.cleaned_data['quantity'] <= i.cleaned_data['product'].quantity:
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
                    raise forms.ValidationError("Too many")


class OrderListInline(admin.TabularInline):
    formset = OrderListTabularFormset
    form = OrderListFormAdmin
    model = OrderList
    extra = 0
    fieldsets = (
        (None, {
            'fields': ('image_product', 'product', 'quantity', 'new_quantity', 'max_quantity', 'price')
        }),
    )
    readonly_fields = ('max_quantity', 'image_product',)
    raw_id_fields = ['product',]


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('status', 'user', 'first_name', 'last_name', 'phone', 'email', 'shipping_price', 'sale', 'payment_method', 'payment_status')
        }),
        ('Address', {
            'classes': ('collapse',),
            'fields': ('country', 'town', 'street', 'postcode', 'company_name')
        }),
        (None, {
            'fields': ('order_notes',)
        })
    )

    list_display = ['id', 'status', 'payment_status', 'first_name']
    list_editable = ['status',]
    search_fields = ['first_name', 'last_name', 'id', 'phone']
    list_filter = ['status']

    inlines = [
        OrderListInline
    ]

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'sale_percent', 'max_uses']
    list_editable = ['max_uses']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Attribute)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Order, OrderAdmin)

admin.site.register(Profile)
