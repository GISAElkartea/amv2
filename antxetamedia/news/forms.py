from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import NewsShow, NewsCategory


class NewsPodcastFilter(forms.Form):
    show = forms.ModelMultipleChoiceField(label=_('Shows'), widget=forms.CheckboxSelectMultiple,
                                          to_field_name='slug', queryset=NewsShow.objects.all())

    category = forms.ModelMultipleChoiceField(label=_('Categories'), widget=forms.CheckboxSelectMultiple,
                                              to_field_name='slug', queryset=NewsCategory.objects.all())
