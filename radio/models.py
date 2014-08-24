from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.utils.translation import ugettext as _


class Category(models.Model):
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    name = models.CharField(max_length=50, verbose_name=_('name'))
    related = models.ManyToManyField('self', verbose_name=_('related categories'))

    def __str__(self):
        return self.name


class Show(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, verbose_name=_('name'))
    # description
    # image
    categories = models.ManyToManyField(Category)
    # tags

    def __str__(self):
        return self.name


class Podcast(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=250, verbose_name=_('title'))
    # description
    # image
    # tags

    # file
    # license
    # embed

    def upload(self):
        pass

    def download(self):
        pass

    def sync(self):
        details = self.download()
        if details is None:
            details = self.upload()
        self.embed = details['embed']
        self.save()

    def __str__(self):
        return self.title


class NewsShow(Show):
    class Meta:
        verbose_name = _('News show')
        verbose_name_plural = _('News shows')


class RadioShow(Show):
    class Meta:
        verbose_name = _('Radio show')
        verbose_name_plural = _('Radio shows')


class ProjectShow(Show):
    class Meta:
        verbose_name = _('Project show')
        verbose_name_plural = _('Project shows')


class NewsPodcast(Podcast):
    class Meta:
        verbose_name = _('News podcast')
        verbose_name_plural = _('News podcasts')

    show = models.ForeignKey(NewsShow, verbose_name=_('show'))


class RadioPodcast(Podcast):
    class Meta:
        verbose_name = _('Radio podcast')
        verbose_name_plural = _('Radio podcasts')

    show = models.ForeignKey(RadioShow, verbose_name=_('show'))


class ProjectPodcast(Podcast):
    class Meta:
        verbose_name = _('Project podcast')
        verbose_name_plural = _('Project podcasts')

    show = models.ForeignKey(ProjectShow, verbose_name=_('show'))


class Playlist(models.Model):
    class Meta:
        unique_together = ('user', 'title')
        verbose_name = _('Playlist')
        verbose_name_plural = _('Playlists')

    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    podcasts = models.ManyToManyField(Podcast, through='PlaylistPosition')


class PlaylistPosition(models.Model):
    class Meta:
        verbose_name = _('Playlist position')
        verbose_name_plural = _('Playlist positions')

    podcast_content_type = models.ForeignKey(ContentType)
    podcast_id = models.PositiveIntegerField()
    podcast = GenericForeignKey('podcast_content_type', 'podcast_id')
    # django-positions
    # position = PositionField()

    def __str__(self):
        return '#{self.position} - {self.podcast}'.format(self)


class UserPreferences(models.Model):
    user = models.OneToOneField(User)
    favorite_radio_shows = models.ManyToManyField(RadioShow)
    favorite_news_shows = models.ManyToManyField(NewsShow)
