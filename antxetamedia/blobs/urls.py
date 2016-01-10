from django.conf.urls import include, url

from .views import PodcastBlobList, admin_async_blob_upload


expressions = {
    'app_label': r'(?P<app_label>[\w-]+)',
    'model': r'(?P<model>[\w-]+)',
    'id': r'(?P<id>\d+)',
    'filename': r'(?P<filename>.+)',
}

news = [
    url(r'^{app_label}/{model}/{id}/$'.format(**expressions), PodcastBlobList.as_view(), name='podcast'),
    url(r'^admin/async_blob_upload/{filename}/$'.format(**expressions), admin_async_blob_upload,
        name='admin_async_blob_upload'),
]

urlpatterns = [url(r'^', include(news, namespace='blobs'))]
