from django.db.models import ImageField, URLField

from hypothesis import Settings
from hypothesis import strategies as st
from hypothesis.extra.django.models import models, add_default_field_mapping

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
import recurrence
from recurrence.fields import RecurrenceField

from antxetamedia.news.models import NewsPodcast, NewsShow
from antxetamedia.radio.models import RadioPodcast, RadioShow, RadioCategory, RadioProducer
from antxetamedia.events.models import Event
from antxetamedia.widgets.models import Widget


Settings.default.max_examples = 1


add_default_field_mapping(AutoSlugField, st.just('some-slug'))
add_default_field_mapping(ImageField, st.just(''))
add_default_field_mapping(RichTextField, st.just(''))
add_default_field_mapping(URLField, st.just('http://example.com/'))
add_default_field_mapping(RecurrenceField, st.just(recurrence.Recurrence(rrules=[recurrence.Rule(recurrence.DAILY)])))


newsshow = models(NewsShow)
newspodcast = models(NewsPodcast, show=newsshow)
radioproducer = models(RadioProducer)
radiocategory = models(RadioCategory)
radioshow = models(RadioShow, category=radiocategory, producer=radioproducer)
radiopodcast = models(RadioPodcast, show=radioshow)
event = models(Event)
widget = models(Widget)
