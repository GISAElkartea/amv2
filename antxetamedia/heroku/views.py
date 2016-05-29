from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.generic import View


CHALLENGES = getattr(settings, 'ACME_CHALLENGES', {})


class AcmeChallenge(View):
    def get(self, request, *args, **kwargs):
        key = CHALLENGES.get(kwargs['token'])
        if key is None:
            raise Http404("Invalid token.")
        return HttpResponse(key)
