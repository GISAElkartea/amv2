import pytz
from itertools import islice
from functools import wraps, total_ordering
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue

from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.six import python_2_unicode_compatible

from autoslug.fields import AutoSlugField
from recurrence.fields import RecurrenceField
from sorl.thumbnail import ImageField


def sliceable(generator):
    @wraps(generator)
    def wrapper(self, *args, **kwargs):
        count = kwargs.pop('count', None)
        iterator = generator(self, *args, **kwargs)
        return iterator if count is None else islice(iterator, count)
    return wrapper


class Naive(object):
    def __init__(self, dt):
        self.dt = dt

    def __enter__(self):
        tz = self.dt.tzinfo
        naive = pytz.UTC.normalize(self.dt).replace(tzinfo=None)
        return naive, tz.localize

    def __exit__(self, *exc):
        pass


class EventQuerySet(models.QuerySet):
    @sliceable
    def after(self, dtstart):
        with Naive(dtstart) as (naive, localize):
            # automatically ordered by date
            queue = PriorityQueue()

            # for every event, get its recurrence after the given datetime
            for e in self.iterator():
                day = e.recurrences.after(naive)
                if day is not None:
                    queue.put((day, e))

            # for every recurrence, get its event and add the next recurrence to the queue
            while not queue.empty():
                day, event = queue.get()
                yield localize(day), event
                day = event.recurrences.after(day)
                if day is not None:
                    queue.put((day, event))

    @sliceable
    def before(self, dtend):
        with Naive(dtend) as (naive, localize):
            # automatically ordered by date
            queue = PriorityQueue()

            # for every event, get its recurrence before the given datetime
            for e in self.iterator():
                day = e.recurrences.before(naive)
                if day is not None:
                    queue.put((day, e))

            # for every recurrence, get its event and add the next recurrence to the queue
            while not queue.empty():
                day, event = queue.get()
                yield localize(day), event
                day = event.recurrences.before(day)
                if day is not None:
                    queue.put((day, event))

    @sliceable
    def between(self, dtstart, dtend):
        with Naive(dtstart) as (naive_start, localize), Naive(dtend) as (naive_end, localize):
            # automatically ordered by date
            queue = PriorityQueue()

            # for every event, get its recurrences between the given datetimes
            for e in self.iterator():
                for day in e.recurrences.between(naive_start, naive_end, inc=True):
                    queue.put((day, e))

            # for every recurrence, get its event and add the next recurrences to the queue
            while not queue.empty():
                day, event = queue.get()
                yield localize(day), event

    @sliceable
    def upcoming(self):
        """
        Get the upcoming event recurrences.
        """
        return self.after(timezone.now().replace(hour=0, minute=0, second=0))


@total_ordering
@python_2_unicode_compatible
class Event(models.Model):
    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    title = models.CharField(_('Title'), max_length=128)
    slug = AutoSlugField(editable=False, unique=True, populate_from='title')

    recurrences = RecurrenceField()
    time = models.TimeField(_('Time'), null=True, blank=True, help_text=_('Leave blank if all day event.'))

    classification = models.CharField(_('Classification'), max_length=1024, blank=True)
    location = models.CharField(_('Location'), max_length=256, blank=True)
    image = ImageField(_('Image'), blank=True, upload_to='events')
    link = models.URLField(_('Link'), blank=True)

    def __str__(self):
        return self.title

    def __lt__(self, other):
        return (self.time, self.pk) < (other.time, other.pk)

    def get_absolute_url(self):
        return reverse('events:detail', kwargs={'slug': self.slug})

    @sliceable
    def upcoming(self):
        """
        Generator of all the future occurrences of this event.
        """
        with Naive(timezone.now()) as (naive, localize):
            upcoming = naive
            while True:
                upcoming = self.recurrences.after(upcoming)
                if upcoming is None:
                    return
                yield localize(upcoming)

    @sliceable
    def past(self):
        """
        Generator of all the past occurrences of this event.
        """
        with Naive(timezone.now()) as (naive, localize):
            past = naive
            while True:
                past = self.recurrences.before(past)
                if past is None:
                    return
                yield localize(past)
