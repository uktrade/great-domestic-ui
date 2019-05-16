import markdown2
from bs4 import BeautifulSoup
from urllib3.util import parse_url

from django.conf import settings


def parse_search_results(content):

    def strip_html(result):
        content = result['content'] if 'content' in result else ''
        html = markdown2.markdown(content)
        result['content'] = ''.join(
            BeautifulSoup(html, "html.parser").findAll(text=True)
        ).rstrip()

    def format_events_url(result):
        if result['type'] == "Event":
            url = parse_url(result['url'])
            result['url'] = settings.HEADER_FOOTER_URLS_EVENTS +\
                url.request_uri

    results = [hit['_source'] for hit in content['hits']['hits']]

    # This removes HTML tags and markdown received from CMS results
    #
    # It first line converts the markdown received into HTML
    # Then we remove HTML tags
    # It also removes unneccessary \n added by the markdown library
    for result in results:
        strip_html(result)
        format_events_url(result)

    # Abridge long text snippets
    for result in results:
        if ('content' in result) and (len(result['content']) > 160):
            result['content'] = result['content'][0:160] + '...'

    return results
