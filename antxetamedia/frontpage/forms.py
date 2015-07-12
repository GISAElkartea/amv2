from django import forms
from django.utils.translation import ugettext_lazy as _

from antxetamedia.news.models import NewsCategory
from antxetamedia.radio.models import RadioShow


class ConfigureFrontPageForm(forms.Form):
    newscategories = forms.ModelMultipleChoiceField(label=_('News Categories'), widget=forms.CheckboxSelectMultiple,
                                                    queryset=NewsCategory.objects.all())

    radioshows = forms.ModelMultipleChoiceField(label=_('Radio Shows'), widget=forms.CheckboxSelectMultiple,
                                                queryset=RadioShow.objects.all())
