from directory_components.forms import DirectoryComponentsFieldMixin

from django import forms


class IntegerField(DirectoryComponentsFieldMixin, forms.IntegerField):
    pass
