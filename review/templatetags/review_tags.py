from django import template

register = template.Library()


@register.inclusion_tag('review/annotate.html', takes_context=True)
def review(context):
    request = context['request']

    return {
        'review_enabled': 'review_token' in request.GET,
        'review_token': request.GET.get('review_token'),
    }
