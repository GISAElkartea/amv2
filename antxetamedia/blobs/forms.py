from django import forms

from .fields import UploadField
from .models import Blob


class BlobForm(forms.ModelForm):
    class Meta:
        model = Blob
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BlobForm, self).__init__(*args, **kwargs)
        self.fields['local'] = UploadField(help_text=self.fields['local'].help_text)
