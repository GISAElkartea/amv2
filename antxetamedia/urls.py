from django.conf import settings
from django.conf.urls import include, url, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin

from .feeds.views import BlobFeed


js_info_dict = {'packages': ['recurrence', 'antxetamedia']}

urlpatterns = [
    url(r'^', include('antxetamedia.frontpage.urls')),
    url(r'^news/', include('antxetamedia.news.urls')),
    url(r'^radio/', include('antxetamedia.radio.urls')),
    url(r'^projects/', include('antxetamedia.projects.urls')),
    url(r'^blobs/', include('antxetamedia.blobs.urls')),
    url(r'^f/', include('antxetamedia.flatpages.urls')),
    url(r'^events/', include('antxetamedia.events.urls')),
    url(r'^schedule/', include('antxetamedia.schedule.urls')),
    url(r'^archive/', include('antxetamedia.archive.urls')),
    url(r'^feed/$', BlobFeed(), name='feed'),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^wkeditor/', include('ckeditor_uploader.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict, name='jsi18n'),
    url(r'^404/$', handler404),
    url(r'^500/$', handler500),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
