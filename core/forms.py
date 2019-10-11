from django import forms as django_forms
from directory_components import forms


class CompaniesHouseSearchForm(django_forms.Form):
    term = django_forms.CharField()


class SectorPotentialForm(forms.Form):
    sector = forms.ChoiceField(
        label='Sector',
        choices=[('', 'To see possible markets - select your sector')],
    )

    def __init__(self, sector_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sorted_sectors = sorted(sector_list, key=lambda x: x['name'])
        self.fields['sector'].choices += [(tag['id'], tag['name']) for tag in sorted_sectors]
