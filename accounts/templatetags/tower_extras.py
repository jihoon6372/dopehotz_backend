from django import template
from django.conf import settings

register = template.Library()

@register.filter
def change_picture(a):
    if a:
        return a.replace('large', 't500x500')


@register.filter
def none_is_blank(text):
    if None is text:
        return ''
    else:
        return text