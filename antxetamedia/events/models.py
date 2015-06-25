import pytz
from Queue import PriorityQueue

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.utils.six import python_2_unicode_compatible

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from recurrence.fields import RecurrenceField


class EventQuerySet(models.QuerySet):
    def upcoming(self, count=None):
        """
        Get the upcoming event recurrences.
        """
        # django-recurrence is not tz aware
        tz = pytz.timezone(settings.TIME_ZONE)
        timezone.activate(tz)
        today = timezone.now().replace(hour=0, minute=0, second=0, tzinfo=None)

        # automatically ordered by date
        upcoming = PriorityQueue()

        # for every event, get its upcoming recurrence
        for e in self.iterator():
            day = e.recurrences.after(today)
            if day is not None:
                upcoming.put((day, e))

        # for every recurrence, get its event and add the next recurrence to the queue
        while (count is None or count > 0) and not upcoming.empty():
            day, event = upcoming.get()
            yield day, event
            if count is not None:
                count -= 1
            day = event.recurrences.after(day)
            if day is not None:
                upcoming.put((day, event))


@python_2_unicode_compatible
class Event(models.Model):
    objects = EventQuerySet.as_manager()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')

    title = models.CharField(_('Title'), max_length=128)
    slug = AutoSlugField(editable=False, unique=True, populate_from='title')

    recurrences = RecurrenceField()
    time = models.TimeField(_('Time'), null=True, blank=True)

    description = RichTextField(_('Description'), blank=True)
    location = models.CharField(_('Location'), max_length=256, blank=True)
    image = models.ImageField(_('Image'), blank=True, upload_to='events')
    link = models.URLField(_('Link'), blank=True)

    def __str__(self):
        return self.title

    def upcoming(self):
        """
        Generator of all the future occurrences of this event.
        """
        utc = timezone.now()
        tz = pytz.timezone(settings.TIME_ZONE)
        naive = utc.replace(tzinfo=None)
        upcoming = naive
        while True:
            upcoming = self.recurrences.after(upcoming)
            if upcoming is None:
                return
            yield tz.localize(upcoming)