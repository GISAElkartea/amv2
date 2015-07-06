from django.conf.urls import include, url

from .views import RadioShowList, RadioShowDetail


expressions = {
    'radioshow': r'(?P<slug>(\w|\d|-)+)',
    'category': r'(?P<slug>(\w|\d|-)+)',
    'producer': r'(?P<slug>(\w|\d|-)+)',
}

radio = [
    url(r'^$', RadioShowList.as_view(), name='list'),
    url(r'^\?category={category}$'.format(**expressions), RadioShowList.as_view(), name='category'),
    url(r'^\?producer={producer}$'.format(**expressions), RadioShowList.as_view(), name='producer'),
    url(r'^{radioshow}/$'.format(**expressions), RadioShowDetail.as_view(), name='detail'),
]

urlpatterns = [url(r'^', include(radio, namespace='radio'))]
