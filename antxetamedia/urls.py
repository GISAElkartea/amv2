from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from .feeds.views import BlobFeed


js_info_dict = {'packages': ['recurrence']}

urlpatterns = [
    url(r'^', include('antxetamedia.frontpage.urls')),
    url(r'^news/', include('antxetamedia.news.urls')),
    url(r'^radio/', include('antxetamedia.radio.urls')),
    url(r'^projects/', include('antxetamedia.projects.urls')),
    url(r'^f/', include('antxetamedia.flatpages.urls')),
    url(r'^events/', include('antxetamedia.events.urls')),
    url(r'^schedule/', include('antxetamedia.schedule.urls')),
    url(r'^archive/', include('antxetamedia.archive.urls')),
    url(r'^feed/$', BlobFeed(), name='feed'),

    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),  # needed by django-recurrence
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
