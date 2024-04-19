from django import template

register = template.Library()


@register.filter
def money(value):
    if value is not None and value != "":
        if value < 0:
            return f"(R$ {-1 * value:.2f})"
        return f"R$ {value:.2f}"


@register.filter(is_safe=False)
def subtract_float(value, arg):
    """Subtract the arg to the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        try:
            return value - arg
        except Exception:
            return ""
