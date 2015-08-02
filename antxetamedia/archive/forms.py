from datetime import datetime

from django import forms
from django.utils import timezone


class EventForm(forms.Form):
    after = forms.DateField(required=False)
    before = forms.DateField(required=False)

    def clean(self):
        data = super(EventForm, self).clean()
        tz = timezone.get_current_timezone()
        if data.get('after'):
            data['after'] = tz.localize(datetime.combine(data['after'], datetime.min.time()))
        if data.get('before'):
            data['before'] = tz.localize(datetime.combine(data['before'], datetime.max.time()))
        return data
