from django import template

register = template.Library()

@register.filter
def check_mod_5(item_id):
    return item_id % 5 == 0