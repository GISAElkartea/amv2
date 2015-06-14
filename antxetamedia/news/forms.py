from antxetamedia.shows.forms import GenericPodcastForm
from .models import NewsShow, NewsPodcast


class NewsPodcastForm(GenericPodcastForm):
    class Meta:
        model = NewsPodcast
        fields = '__all__'
        related_queryset = NewsShow.objects.values_list('pk', 'name')
