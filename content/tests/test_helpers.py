import pytest
from content.helpers import unslugify

unslugify_slugs = [
    ('test-slug-one', 'Test slug one'),
    ('test-two', 'Test two'),
    ('slug', 'Slug'),
]


@pytest.mark.parametrize('slug,exp', unslugify_slugs)
def test_unslugify(slug, exp):
    assert unslugify(slug) == exp
