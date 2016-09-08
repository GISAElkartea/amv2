# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.forms import widgets
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.core.files.storage import default_storage


class UploadWidget(widgets.TextInput):
    link = '<a href="{link}" target="_blank">{view}</a>'
    widget = '<p>{input}<span>{link}</span><br><input type="file" onchange="{script}" value="upload"></p>'
    script = "GetBlobUploader('{upload_url}', '{media_url}', '{pending}', '{view}')(this);"

    class Media:
        js = ['js/blob_uploader.js']

    def __init__(self, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        attrs['readonly'] = 'readonly'
        super(UploadWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        input = super(UploadWidget, self).render(name, value, attrs=attrs)
        link = getattr(value, 'url', None) if value else None
        link = '' if link is None else self.link.format(link=link, view=_('Listen'))
        upload_url = reverse('blobs:admin_async_blob_upload', kwargs={'filename': 'filename'})
        media_url = default_storage.url('filename')
        script = self.script.format(upload_url=upload_url, media_url=media_url,
                                    pending=_('Pending…'), view=_('Listen'))
        return mark_safe(self.widget.format(input=input, link=link, script=script, view=_('Listen')))
