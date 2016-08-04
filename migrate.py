#!/usr/bin/env python

import os
import logging
from dateutil.parser import parse

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "antxetamedia.settings")
django.setup()

from django.db.models import Max
from django.utils.timezone import make_aware
from django.contrib.contenttypes.models import ContentType

from antxetamedia.news.models import NewsCategory, NewsPodcast, NewsShow
from antxetamedia.blobs.models import Blob, Account


ACCOUNT_NAME = 'archive.org'


def filter_model(data, model):
    return (obj for obj in data if obj['model'] == model)


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
                                                      description=np['fields']['text'],
                                                      pub_date=make_aware(parse(np['fields']['pub_date'])),
                                                      image=np['fields']['image'],
                                                      show=default_show)
        else:
            logging.debug("Ignoring NewsPodcast with slug {}.".format(np['fields']['slug']))

        news_podcast.categories = [news_category_correspondence[pk] for pk in np['fields']['categories']]
        pk_old_to_new[np['pk']] = news_podcast.pk

    return pk_old_to_new


def import_news_blobs(news_blobs, news_podcast_correspondence):
    news_podcast_ct = ContentType.objects.get_for_model(NewsPodcast)
    account = Account.objects.get(name=ACCOUNT_NAME)

    pk_old_to_new = {}
    for nb in news_blobs:
        try:
            news_blob = Blob.objects.get(remote=nb['fields']['remote'])
        except Blob.DoesNotExist:
            logging.info("Importing Blob with remote {}.".format(nb['fields']['remote']))
            siblings = Blob.objects.filter(content_type=news_podcast_ct,
                                           object_id=news_podcast_correspondence[nb['fields']['object_id']])
            position = siblings.aggregate(position=Max('position'))['position']
            position = 0 if position is None else position + 1

            news_blob = Blob.objects.create(content_type=news_podcast_ct,
                                            object_id=news_podcast_correspondence[nb['fields']['object_id']],
                                            position=position,
                                            remote=nb['fields']['remote'],
                                            account=account)
        else:
            logging.debug("Ignoring Blob with remote {}.".format(nb['fields']['remote']))

        pk_old_to_new[nb['pk']] = news_blob.pk
    return pk_old_to_new


def import_news(objects):
    nc = filter_model(objects, 'recordings.newscategory')
    nc_correspondence = import_news_categories(nc)
    np = filter_model(objects, 'recordings.news')
    np_correspondence = import_news_podcasts(np, nc_correspondence)
    nb = filter_model(objects, 'multimedia.media')
    nb = (b for b in nb if (b['fields']['content_type'] == ['recordings', 'news'] and
                            b['fields']['remote'] and
                            b['fields']['remote'].startswith('http')))
    import_news_blobs(nb, np_correspondence)


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
        sys.stderr.write('{} [-v] ([news] [radio] [projects] [agenda])\n'.format(sys.argv[0]))
    if 'news' in sys.argv[1:]:
        import_news(objects)
    if 'radio' in sys.argv[1:]:
        import_radio(objects)
