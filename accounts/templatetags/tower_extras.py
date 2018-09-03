from django import template

register = template.Library()

@register.filter
def change_picture(a):
    return a.replace('large', 't500x500')