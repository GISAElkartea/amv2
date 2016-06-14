import base64
import os

from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import ListView

from .models import Blob


class PodcastBlobList(ListView):
    def get_queryset(self):
        qs = Blob.objects.with_content()
        qs = qs.filter(content_type__app_label=self.kwargs['app_label'],
                       content_type__model=self.kwargs['model'],
                       object_id=self.kwargs['id'])
        qs = qs.order_by('position')
        qs = qs.select_related('content_type').prefetch_related('content_object')
        return qs

    def get_blob_data(self, blob):
        return {
            'pk': blob.pk,
            'podcast': blob.content_object.get_absolute_url(),
            'title': str(blob),
            'image': blob.content_object.image.url if blob.content_object.image else None,
            'url': blob.link,
        }

    def get_context_data(self, **kwargs):
        kwargs['blob_list'] = [self.get_blob_data(blob) for blob in self.object_list]
        return super(PodcastBlobList, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse({'blobs': context['blob_list']})


@staff_member_required
def admin_async_blob_upload(request, filename):
    filename = base64.b64decode(filename).decode('utf-8')
    path = os.path.join(Blob._meta.get_field('local').get_directory_name(), filename)
    return HttpResponse(default_storage.save(path, ContentFile(request.body)), 'text/plain')
