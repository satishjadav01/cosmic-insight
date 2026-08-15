from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
@register.filter
def replace(value, arg):
    try:
        old, new = arg.split(':')
        return value.replace(old, new)
    except:
        return value
@register.filter
def index(sequence, position):
    try:
        return sequence[position]
    except:
        return ''
