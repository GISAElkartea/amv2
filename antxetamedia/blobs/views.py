from django.http import JsonResponse
from django.views.generic import ListView

from .models import Blob


class PodcastBlobList(ListView):
    model = Blob

    def get_queryset(self):
        qs = super(PodcastBlobList, self).get_queryset()
        qs = qs.filter(content_type__app_label=self.kwargs['app_label'],
                       content_type__model=self.kwargs['model'],
                       object_id=self.kwargs['id'])
        qs = qs.order_by('-position')
        qs = qs.select_related('content_type').prefetch_related('content_object')
        return qs

    def get_blob_data(self, blob):
        return {
            'id': blob.pk,
            'podcast': blob.content_object.get_blobs_url(),
            'title': blob.content_object.title,
            'image': blob.content_object.image.url if blob.content_object.image else None,
            'url': blob.link,
        }

    def get_context_data(self, **kwargs):
        kwargs['blob_list'] = [self.get_blob_data(blob) for blob in self.object_list]
        return super(PodcastBlobList, self).get_context_data(**kwargs)

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context['blob_list'], safe=False)
