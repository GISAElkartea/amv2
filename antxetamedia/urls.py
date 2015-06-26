from django.conf.urls import include, url
from django.contrib import admin

js_info_dict = {'packages': ['recurrence']}

urlpatterns = [
    url(r'^', include('antxetamedia.frontpage.urls')),
    url(r'^news/', include('antxetamedia.news.urls')),
    url(r'^radio/', include('antxetamedia.radio.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),  # needed by django-recurrence
]
