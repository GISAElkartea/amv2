from django.forms import fields, widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage


class UploadWidget(widgets.TextInput):
    widget = ('<p>{input}<span><a href="{link}" target="_blank">{view}</a></span><br>'
              '<input type="file" onchange="{script}" value="upload"></p>')
    script = "GetBlobUploader('{upload_url}', '{media_url}', '{pending}', '{view}')(this);"

    class Media:
        js = ['js/blob_uploader.js']

    def __init__(self, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        attrs['readonly'] = 'readonly'
        super(UploadWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        attrs = attrs or {}
        attrs['class'] = 'vTextField'
        input = super(UploadWidget, self).render(name, value, attrs=attrs)
        link = getattr(value, 'url', None) or value
        upload_url = reverse('blobs:admin_async_blob_upload', kwargs={'filename': 'filename'})
        media_url = default_storage.url('filename')
        script = self.script.format(upload_url=upload_url, media_url=media_url,
                                    pending=_('Pending…'), view=_('Listen'))
        return mark_safe(self.widget.format(input=input, link=link, script=script, view=_('Listen')))


class UploadField(fields.CharField):
    widget = UploadWidget
