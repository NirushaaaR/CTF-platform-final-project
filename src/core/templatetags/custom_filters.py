from django import template

register = template.Library()


@register.filter
def get_dict_value(dict_instance, key):
    return dict_instance.get(key)