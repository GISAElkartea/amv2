from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import View


KEY = getattr(settings, 'ACME_KEY', None)
TOKEN = getattr(settings, 'ACME_TOKEN', None)


class AcmeChallenge(View):
    def get(self, request, *args, **kwargs):
        if kwargs['token'] != TOKEN:
            raise Http404()
        return HttpResponse(KEY)
