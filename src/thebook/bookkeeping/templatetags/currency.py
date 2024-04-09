from django import template

register = template.Library()


@register.filter
def money(value):
    if value is not None:
        if value < 0:
            return f"(R$ {-1 * value:.2f})"
        return f"R$ {value:.2f}"
