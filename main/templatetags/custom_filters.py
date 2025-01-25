# your_app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def remove_text(value):
    return value.split("\n")[0] if value.split("\n")[0] in value else value