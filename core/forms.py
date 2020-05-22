from directory_components import forms
from directory_constants import urls

from django.template.loader import render_to_string
from django.utils.html import mark_safe

from core import constants


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    f'<a href="{urls.domestic.TERMS_AND_CONDITIONS}" target="_blank">terms and '
    'conditions</a> of the great.gov.uk service.'
)

PRIVACY_POLICY_URL = urls.domestic.PRIVACY_AND_COOKIES / 'privacy-notice-great-domestic'

CONSENT_CHOICES = (
    (constants.CONSENT_EMAIL, 'I would like to receive additional information by email'),
    (constants.CONSENT_PHONE, ' I would like to receive additional information by telephone'),
)


class CompaniesHouseSearchForm(forms.Form):
    term = forms.CharField()


class SectorPotentialForm(forms.Form):

    SECTOR_CHOICES_BASE = [('', 'Select your sector')]

    sector = forms.ChoiceField(
        label='Sector',
        choices=SECTOR_CHOICES_BASE,
    )

    def __init__(self, sector_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorted_sectors = sorted(sector_list, key=lambda x: x['name'])
        self.fields['sector'].choices = (
            self.SECTOR_CHOICES_BASE + [(tag['name'], tag['name']) for tag in sorted_sectors]
        )


class ConsentFieldMixin(forms.Form):
    contact_consent = forms.MultipleChoiceField(
        label=render_to_string('core/contact-consent.html', {'privacy_url': PRIVACY_POLICY_URL}),
        widget=forms.CheckboxSelectInlineLabelMultiple(attrs={'id': 'checkbox-multiple'}, use_nice_ids=True),
        choices=CONSENT_CHOICES
    )

    @staticmethod
    def move_to_end(fields, name):
        fields.remove(name)
        fields.append(name)

    def order_fields(self, field_order):
        # move terms agreed and captcha to the back
        field_order = field_order or list(self.fields.keys())
        field_order = field_order[:]
        self.move_to_end(fields=field_order, name='contact_consent')
        if 'captcha' in field_order:
            self.move_to_end(fields=field_order, name='captcha')
        return super().order_fields(field_order)
