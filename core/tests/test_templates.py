from directory_components.context_processors import urls_processor

from django.template.loader import render_to_string


def test_error_templates(rf):
    template_name = '404.html'
    assert render_to_string(template_name, {'request': rf.get('/')})


def test_404_custom_template(settings, client):
    settings.DEBUG = False
    response = client.get('/this-is-not-a-valid-url/')
    assert response.status_code == 404
    expected_text = bytes(
        'If you entered a web address please check'
        ' it’s correct.', 'utf8')
    assert expected_text in response.content


def test_about_page_services_links(settings):
    context = urls_processor(None)
    html = render_to_string('core/about.html', context)
    assert settings.DIRECTORY_CONSTANTS_URL_FIND_A_BUYER in html
    assert settings.DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS in html
