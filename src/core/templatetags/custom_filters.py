from django import template

register = template.Library()


@register.filter
def get_dict_value(dict_instance, key):
    if dict_instance is None:
        return None
    return dict_instance.get(key)


@register.filter
def censor_flag(flag: str):
    """ Make Flag format FLAG{----------} """
    if flag.startswith("FLAG{") and flag.endswith("}"):
        return "FLAG{" + ("-" * (len(flag) - 6)) + "}"
    return "-" * len(flag)
