from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('antxetamedia.frontpage.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
