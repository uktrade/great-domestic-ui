from django import template
import jwt

register = template.Library()


@register.inclusion_tag('review/annotate.html', takes_context=True)
def review(context):
    request = context['request']


    if 'review_token' in request.GET:
        review_token = request.GET['review_token']

        # No need to verify as we only beed the reviewer name for display purposes
        decoded = jwt.decode(review_token, verify=False)

        return {
            'review_enabled': True,
            'review_token': review_token,
            'reviewer_name': decoded['reviewer_name'],
        }
    else:
        return {
            'review_enabled': False,
            'review_token': None,
            'reviewer_name': '',
        }
