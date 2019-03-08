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
    description = page.get('article_teaser')
    if not description:
        description = ''.join(BeautifulSoup(
            page.get('article_body_text')
        ).findAll(text=True))[:META_DESCRIPTION_TEXT_LENGTH]
    return description
