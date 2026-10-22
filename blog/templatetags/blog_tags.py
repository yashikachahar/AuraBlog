import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ""
    # Render markdown with code highlighting and tables
    html = markdown.markdown(text, extensions=['extra', 'nl2br', 'sane_lists'])
    return mark_safe(html)

@register.filter(name='reading_time')
def reading_time_filter(minutes):
    if not minutes or minutes <= 1:
        return "1 min read"
    return f"{minutes} min read"
