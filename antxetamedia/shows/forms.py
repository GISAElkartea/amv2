from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


class GenericPodcastForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GenericPodcastForm, self).__init__(*args, **kwargs)
        self.related_queryset = getattr(self.Meta, 'related_queryset', None)
        if self.related_queryset is not None:
            # Set the default show type and hide it -- quircks with Meta subclassing
            self.related_type = ContentType.objects.get_for_model(self.related_queryset.model)
            self.fields['show_type'].initial = self.related_type
            self.fields['show_type'].widget = forms.HiddenInput()
            # Create a show selector
            choices = BLANK_CHOICE_DASH + list(self.related_queryset)
            self.fields['show_id'] = forms.ChoiceField(label=_('Show'), choices=choices)

    def save(self, *args, **kwargs):
        if self.related_queryset is not None:
            # Doesn't matter if the user messes with the hidden show type field, we reset it
            self.instance.show_type = self.related_type
        return super(GenericPodcastForm, self).save(*args, **kwargs)
