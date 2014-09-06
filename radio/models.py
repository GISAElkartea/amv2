from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ckeditor.fields import RichTextField
from positions.fields import PositionField
from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager


class Category(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Show(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = RichTextField(blank=True)
    image = ImageField(upload_to='shows', blank=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


class Podcast(models.Model):
    class Meta:
        abstract = True

    title = models.CharField(max_length=250, verbose_name=_('title'))
    description = RichTextField(blank=True)
    image = ImageField(upload_to='podcasts', blank=True)
    tags = TaggableManager(blank=True)

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


class NewsCategory(Category):
    class Meta:
        verbose_name = _('News category')
        verbose_name_plural = _('News categories')


class NewsShow(Show):
    class Meta:
        verbose_name = _('News show')
        verbose_name_plural = _('News shows')

    categories = models.ManyToManyField(NewsCategory, blank=True)


class NewsPodcast(Podcast):
    class Meta:
        verbose_name = _('News podcast')
        verbose_name_plural = _('News podcasts')

    show = models.ForeignKey(NewsShow, verbose_name=_('show'))


class RadioCategory(Category):
    class Meta:
        verbose_name = _('Radio category')
        verbose_name_plural = _('Radio categories')


class RadioShow(Show):
    class Meta:
        verbose_name = _('Radio show')
        verbose_name_plural = _('Radio shows')

    categories = models.ManyToManyField(RadioCategory, blank=True)


class RadioPodcast(Podcast):
    class Meta:
        verbose_name = _('Radio podcast')
        verbose_name_plural = _('Radio podcasts')

    show = models.ForeignKey(RadioShow, verbose_name=_('show'))


class ProjectCategory(Category):
    class Meta:
        verbose_name = _('Project category')
        verbose_name_plural = _('Project categories')


class ProjectShow(Show):
    class Meta:
        verbose_name = _('Project show')
        verbose_name_plural = _('Project shows')

    categories = models.ManyToManyField(ProjectCategory, blank=True)


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

    def __str__(self):
        return self.title

    def get_list_url(self):
        return reverse('playlist-list')

    def get_absolute_url(self):
        return reverse('playlist-detail', kwargs={'pk': self.pk})

    def get_podcasts_url(self):
        return reverse('playlist-element-list', kwargs={
            'parent_lookup_playlist': self.pk})


class PlaylistElement(models.Model):
    class Meta:
        ordering = ('position',)
        verbose_name = _('Playlist element')
        verbose_name_plural = _('Playlist element')

    playlist = models.ForeignKey(Playlist, related_name='elements')
    podcast_content_type = models.ForeignKey(ContentType)
    podcast_id = models.PositiveIntegerField()
    podcast = GenericForeignKey('podcast_content_type', 'podcast_id')
    position = PositionField(default=0)

    def get_list_url(self):
        return self.playlist.get_podcasts_url()

    def get_absolute_url(self):
        return reverse('playlist-element-detail', kwargs={
            'parent_lookup_playlist': self.playlist.pk, 'pk': self.pk})


class UserPreferences(models.Model):
    user = models.OneToOneField(User)
    favorite_radio_shows = models.ManyToManyField(RadioShow)
    favorite_news_shows = models.ManyToManyField(NewsShow)
