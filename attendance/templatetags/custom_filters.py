from django import template

register = template.Library()

@register.filter
def split_by_dot(value):
    if not value:
        return "-"
    parts = [p.strip() for p in value.split('.') if p.strip()]
    return '<br>'.join(parts) + ('.' if value.strip().endswith('.') else '')
