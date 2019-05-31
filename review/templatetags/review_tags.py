from django import template

register = template.Library()


@register.inclusion_tag('review/annotate.html', takes_context=True)
def review(context):
    return {
        'review_enabled': True,
    }
