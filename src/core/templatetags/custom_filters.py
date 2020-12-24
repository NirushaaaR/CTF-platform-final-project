from django import template

register = template.Library()


@register.filter
def get_dict_value(dict_instance, key):
    if dict_instance is None:
        return None
    return dict_instance.get(key)

def replace_char(char):
    return char if char == "_" else "*"

@register.filter
def censor_flag(flag: str):
    """ Make Flag format FLAG{----------} """
    if not flag:
        return ""
    elif flag.startswith("FLAG{") and flag.endswith("}"):
        return "FLAG{"+''.join([replace_char(char) for char in flag[4:-1]])+"}"
    return "-" * len(flag)