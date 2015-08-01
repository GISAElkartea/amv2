from django import forms


class EventForm(forms.Form):
    before = forms.DateField()
    after = forms.DateField()
