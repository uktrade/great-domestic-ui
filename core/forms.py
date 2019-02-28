from django import forms


class CompaniesHouseSearchForm(forms.Form):
    term = forms.CharField()
