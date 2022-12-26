from django import template
register = template.Library()

@register.filter
def range_list(number):
    return range(number)

@register.filter
def range_list_minus(number):
    return range(5 - number)