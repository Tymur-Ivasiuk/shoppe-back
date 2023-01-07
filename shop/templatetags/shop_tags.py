from django import template
register = template.Library()

@register.filter
def range_list(number):
    return range(number)

@register.filter
def range_list_minus(number):
    return range(5 - number)

@register.filter
def get_item(dictionary, value):
    try:
        return dictionary.get(str(value)) if dictionary.get(str(value)) else {}
    except:
        return {}


@register.filter
def sum_subtotal(dictionary):
    summa = 0
    for i in dictionary.values():
        summa += i['quantity']*i['price']
    return summa

@register.filter
def item_sum(dictionary):
    return dictionary['quantity']*dictionary['price']

@register.filter
def minus(number, value):
    return number-value

@register.filter
def with_sale(number, value):
    return number * (100 - value) / 100 if value else number

@register.filter
def sale(number, value):
    return number/100*value

