from django import forms as django_forms
from directory_components import forms


class CompaniesHouseSearchForm(django_forms.Form):
    term = django_forms.CharField()


class SectorPotentialForm(forms.Form):

    SECTOR_CHOICES_BASE = [('', 'Select your sector')]

    sector = forms.ChoiceField(
        label='Sector',
        choices=SECTOR_CHOICES_BASE,
    )

    def __init__(self, sector_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorted_sectors = sorted(sector_list, key=lambda x: x['name'])
        self.fields['sector'].choices = self.SECTOR_CHOICES_BASE + [(tag['id'], tag['name']) for tag in sorted_sectors]
