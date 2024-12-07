from django import template

register = template.Library()

@register.filter
def truncate_chars(value, num_chars):
    """Truncates a string after a certain number of characters."""
    if len(value) > num_chars:
        return value[:num_chars] + '...'
    return value
