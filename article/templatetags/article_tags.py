import dateparser
from bs4 import BeautifulSoup

from django import template

register = template.Library()


@register.filter
def parse_date(date_string):
    if date_string:
        return dateparser.parse(date_string).strftime('%d %B %Y')
    return None


META_DESCRIPTION_TEXT_LENGTH = 150


@register.simple_tag
def get_meta_description(page, **kwargs):
    search_description = page.get('search_description', '')
    description = page.get('article_teaser', search_description)
    if not description and page.get('article_body_text'):
        html = BeautifulSoup(page.get('article_body_text'), 'html.parser')
        body_text = html.findAll(text=True)
        description = ''.join(body_text)[:META_DESCRIPTION_TEXT_LENGTH]
    return description
