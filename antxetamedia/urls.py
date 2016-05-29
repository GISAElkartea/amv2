from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.i18n import javascript_catalog

from .feeds.views import BlobFeed
from .heroku.views import AcmeChallenge


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
    url(r'^jsi18n/$', javascript_catalog, js_info_dict, name='jsi18n'),
    url(r'^404/$', TemplateView.as_view(template_name='404.html')),
    url(r'^500/$', TemplateView.as_view(template_name='500.html')),
    url(r'^.well-known/acme-challenge/(?P<token>.+)/$', AcmeChallenge.as_view())
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
