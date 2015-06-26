from django.conf.urls import include, url

from .views import NewsPodcastList, NewsPodcastDetail


expressions = {
    'newspodcast': r'(?P<slug>(\w|\d|-)+)',
    'show': r'(?P<slug>(\w|\d|-)+)',
    'category': r'(?P<slug>(\w|\d|-)+)',
}

news = [
    url(r'^$', NewsPodcastList.as_view(), name='list'),
    url(r'^\?show={show}$'.format(**expressions), NewsPodcastList.as_view(), name='show'),
    url(r'^\?category={category}$'.format(**expressions), NewsPodcastList.as_view(), name='category'),
    url(r'^{newspodcast}/$'.format(**expressions), NewsPodcastDetail.as_view(), name='detail'),
]

urlpatterns = [url(r'^', include(news, namespace='news'))]
