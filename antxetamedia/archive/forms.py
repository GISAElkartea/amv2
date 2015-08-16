from datetime import datetime

from django import forms
from django.utils import timezone, formats
from django.utils.translation import ugettext as _


class PikadayWidget(forms.DateInput):
    class Media:
        js = [
            'bower_components/momentjs/moment.js',
            'bower_components/pikaday/pikaday.js',
            'js/pikaday.js',
        ]
        css = {'all': ['bower_components/pikaday/css/pikaday.css']}

    def __init__(self, attrs=None, format=None):
        final_attrs = {'class': 'pikaday'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(PikadayWidget, self).__init__(attrs=final_attrs, format=format)


class PikadayDateField(forms.DateField):
    widget = PikadayWidget


class PikadayDateTimeHiddenTimeField(forms.DateTimeField):
    widget = PikadayWidget
    input_formats = formats.get_format_lazy('DATE_INPUT_FORMATS')
    default_error_messages = {
        'invalid': _('Enter a valid date.'),
    }


class EventForm(forms.Form):
    after = PikadayDateField(required=False)
    before = PikadayDateField(required=False)

    def clean(self):
        data = super(EventForm, self).clean()
        tz = timezone.get_current_timezone()
        if data.get('after'):
            data['after'] = tz.localize(datetime.combine(data['after'], datetime.min.time()))
        if data.get('before'):
            data['before'] = tz.localize(datetime.combine(data['before'], datetime.max.time()))
        return data
