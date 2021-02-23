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
        return "FLAG{" + "".join([replace_char(char) for char in flag[4:-1]]) + "}"
    return "-" * len(flag)


@register.filter
def render_docker_url(url, path):
    """ render docker url whether / or no / """
    return f"{url}{path}" if path.startswith("/") else f"{url}/{path}"


@register.filter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False

@register.simple_tag
def render_url_with_param(path, param, value):
    """ generate a GET PARAM url by looking to at & ot ? """
    print(path)
    if "?" in path:
        return f"{path}&{param}={value}"
    else:
        return f"{path}?{param}={value}"