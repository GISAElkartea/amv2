#!/usr/bin/env python

import os
import logging
from dateutil.parser import parse

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antxetamedia.settings")
django.setup()

from django.apps import apps
from django.db.models import Max
from django.utils.timezone import make_aware
from django.contrib.contenttypes.models import ContentType

from recurrence import Recurrence

from antxetamedia.news.models import NewsCategory, NewsPodcast, NewsShow
from antxetamedia.blobs.models import Blob, Account
from antxetamedia.projects.models import ProjectProducer, ProjectShow, ProjectPodcast
from antxetamedia.events.models import Event


ACCOUNT_NAME = 'archive.org'


def filter_model(data, model):
    return (obj for obj in data if obj['model'] == model)


def filter_blobs(data, content_type):
    return (obj for obj in data if (obj['model'] == 'multimedia.media' and
                                    obj['fields']['content_type'] == content_type.split('.') and
                                    obj['fields']['remote'] and
                                    obj['fields']['remote'].startswith('http')))


def import_blobs(blobs, content_type, correspondence):
    content_type = ContentType.objects.get_for_model(apps.get_model(content_type))
    account = Account.objects.get(name=ACCOUNT_NAME)

    pk_old_to_new = {}
    for b in blobs:
        remote = b['fields']['remote']
        try:
            blob = Blob.objects.get(remote=remote)
        except Blob.DoesNotExist:
            logging.info("Importing Blob with remote {}.".format(remote))
            object_id = correspondence[b['fields']['object_id']]
            siblings = Blob.objects.filter(content_type=content_type, object_id=object_id)
            position = siblings.aggregate(position=Max('position'))['position']
            position = 0 if position is None else position + 1
            blob = Blob.objects.create(content_type=content_type, object_id=object_id, position=position,
                                       remote=remote, account=account)
        else:
            logging.debug("Ignoring Blob with remote {}.".format(remote))

        pk_old_to_new[b['pk']] = blob.pk
    return pk_old_to_new


def import_news_categories(news_categories):
    pk_old_to_new = {}
    for nc in news_categories:
        try:
            news_category = NewsCategory.objects.get(slug=nc['fields']['slug'])
        except NewsCategory.DoesNotExist:
            logging.info("Importing NewsCategory with slug {}.".format(nc['fields']['slug']))
            news_category = NewsCategory.objects.create(name=nc['fields']['name'],
                                                        slug=nc['fields']['slug'])
        else:
            logging.debug("Ignoring NewsCategory with slug {}.".format(nc['fields']['slug']))
        pk_old_to_new[nc['pk']] = news_category.pk
    return pk_old_to_new


def import_news_podcasts(news_podcasts, news_category_correspondence):
    pk_old_to_new = {}
    default_show, _ = NewsShow.objects.get_or_create(name='Antxeta Irratia',
                                                     slug='antxeta-irratia')
    for np in news_podcasts:
        try:
            news_podcast = NewsPodcast.objects.get(slug=np['fields']['slug'])
        except NewsPodcast.DoesNotExist:
            logging.info("Importing NewsPodcast with slug {}.".format(np['fields']['slug']))
            news_podcast = NewsPodcast.objects.create(title=np['fields']['title'],
                                                      slug=np['fields']['slug'],
                                                      description=np['fields']['_text_rendered'],
                                                      pub_date=make_aware(parse(np['fields']['pub_date'])),
                                                      image=np['fields']['image'],
                                                      show=default_show)
        else:
            logging.debug("Ignoring NewsPodcast with slug {}.".format(np['fields']['slug']))

        news_podcast.categories = [news_category_correspondence[pk] for pk in np['fields']['categories']]
        pk_old_to_new[np['pk']] = news_podcast.pk

    return pk_old_to_new


def import_news(objects):
    nc = filter_model(objects, 'recordings.newscategory')
    nc_correspondence = import_news_categories(nc)
    np = filter_model(objects, 'recordings.news')
    np_correspondence = import_news_podcasts(np, nc_correspondence)
    nb = filter_blobs(objects, 'recordings.news')
    import_blobs(nb, 'news.NewsPodcast', np_correspondence)


def import_project_shows(project_shows):
    default_producer, _ = ProjectProducer.objects.get_or_create(name='Antxeta Irratia',
                                                                slug='antxeta-irratia')
    pk_old_to_new = {}
    for ps in project_shows:
        try:
            project_show = ProjectShow.objects.get(slug=ps['fields']['slug'])
        except ProjectShow.DoesNotExist:
            logging.info("Importing ProjectShow with slug {}.".format(ps['fields']['slug']))
            project_show = ProjectShow.objects.create(name=ps['fields']['name'],
                                                      slug=ps['fields']['slug'],
                                                      producer=default_producer,
                                                      creation_date=ps['fields']['beginning'],
                                                      description=ps['fields']['_text_rendered'],
                                                      image=ps['fields']['image'])
        else:
            logging.debug("Ignoring ProjectShow with slug {}.".format(ps['fields']['slug']))
        pk_old_to_new[ps['pk']] = project_show.pk
    return pk_old_to_new


def import_project_podcasts(project_blobs, project_show_correspondence):
    pk_old_to_new = {}
    for pb in project_blobs:
        try:
            project_podcast = ProjectPodcast.objects.get(title=pb['fields']['title'])
        except ProjectPodcast.DoesNotExist:
            logging.info("Importing ProjectPodcast with title {}.".format(pb['fields']['title']))
            show_id = project_show_correspondence[pb['fields']['object_id']]
            project_podcast = ProjectPodcast.objects.create(title=pb['fields']['title'],
                                                            show=ProjectShow.objects.get(pk=show_id))
        else:
            logging.debug("Ignoring ProjectPodcast with title {}.".format(pb['fields']['title']))
        pk_old_to_new[pb['fields']['object_id']] = project_podcast.pk
    return pk_old_to_new


def import_projects(objects):
    ps = filter_model(objects, 'projects.project')
    ps_correspondence = import_project_shows(ps)
    pb = filter_blobs(objects, 'projects.project')
    pp_correspondence = import_project_podcasts(pb, ps_correspondence)
    import_blobs(pb, 'projects.ProjectPodcast', pp_correspondence)


def import_events(objects):
    towns = {t['pk']: t['fields']['name'] for t in filter_model(objects, 'agenda.town')}
    for e in filter_model(objects, 'agenda.happening'):
        try:
            Event.objects.get(slug=e['fields']['slug'])
        except Event.DoesNotExist:
            logging.info("Importing Event with slug {}.".format(e['fields']['slug']))
            location = e['fields']['other_town'] if e['fields']['other_town'] else towns.get(e['fields']['town'], '')
            if location and e['fields']['place']:
                location += ' - '
            location += e['fields']['place']
            recurrences = Recurrence(rdates=[make_aware(parse(e['fields']['date']))])
            Event.objects.create(title=e['fields']['name'],
                                 slug=e['fields']['slug'],
                                 time=e['fields']['time'],
                                 description=e['fields']['_description_rendered'],
                                 location=location,
                                 recurrences=recurrences,
                                 link=e['fields']['link'])
        else:
            logging.debug("Ignoring Event with slug {}.".format(e['fields']['slug']))


def import_radio(objects):
    pass


if __name__ == '__main__':
    import json
    import sys

    data = sys.stdin.read()
    objects = json.loads(data)

    args = set(sys.argv[1:])
    level = logging.DEBUG if '-v' in args else logging.INFO
    logging.basicConfig(level=level)
    args.discard('-v')
    if not args:
        sys.stderr.write('{} [-v] ([news] [radio] [projects] [events])\n'.format(sys.argv[0]))
    if 'news' in args:
        import_news(objects)
    if 'projects' in args:
        import_projects(objects)
    if 'events' in args:
        import_events(objects)
    if 'radio' in args:
        import_radio(objects)
