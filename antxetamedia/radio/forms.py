from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import RadioCategory, RadioProducer


class RadioShowFilter(forms.Form):
    category = forms.ModelMultipleChoiceField(label=_('Categories'), widget=forms.CheckboxSelectMultiple,
                                              to_field_name='slug', queryset=RadioCategory.objects.all())

    producer = forms.ModelMultipleChoiceField(label=_('Producers'), widget=forms.CheckboxSelectMultiple,
                                              to_field_name='slug', queryset=RadioProducer.objects.all())
