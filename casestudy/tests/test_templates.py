from django.template.loader import render_to_string

from directory_constants import urls
from directory_components.context_processors import urls_processor
from bs4 import BeautifulSoup

from casestudy import casestudies


def test_case_study_soo_link(settings):
    context = urls_processor(None)
    context['casestudy'] = casestudies.HELLO_BABY
    html = render_to_string('casestudy/hello-baby.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    soo_link = soup.find(string='Selling online overseas service').parent

    assert soo_link.attrs['href'] == urls.SERVICES_SOO
