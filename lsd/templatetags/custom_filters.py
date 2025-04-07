from django import template
import re

register = template.Library()

@register.filter
def regex_match(value, pattern):
    """
    Check if a string matches a regex pattern.
    Usage: {{ value|regex_match:"pattern" }}
    """
    if not value:
        return False
    try:
        return bool(re.match(pattern, str(value)))
    except re.error:
        return False 