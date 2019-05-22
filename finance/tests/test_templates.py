from django.template.loader import render_to_string
from django.urls import reverse


def test_get_finance_template():
    context = {}
    html = render_to_string('finance/trade_finance.html', context)

    expected = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': 'contact'}
    )

    assert expected in html
