from django.template.loader import render_to_string
from directory_components.context_processors import urls_processor


def test_cms_guidance_descriptive_page_title_is_rendered(rf, context):

    context['request'] = rf.get('/')
    page = {
        'title': 'Descriptive text',
    }

    context['page'] = page
    html = render_to_string('contact/guidance.html', context)

    assert page['title'] + ' - great.gov.uk' in html


def test_contact_domestic_descriptive_page_title_override_is_rendered(context):
    context = urls_processor(None)
    html = render_to_string('contact/domestic/step.html', context)

    assert 'Tell us how we can help - great.gov.uk' in html
