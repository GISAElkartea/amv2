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


def import_news(objects):
    # Import news categories

    for nc in filter_model(objects, 'recordings.newscategory'):
        if NewsCategory.objects.filter(slug=nc['fields']['slug']).exists():
            logging.debug("Ignoring NewsCategory with slug {}.".format(nc['fields']['slug']))
        else:
            logging.info("Importing NewsCategory with slug {}.".format(nc['fields']['slug']))
            NewsCategory.objects.create(name=nc['fields']['name'],
                                        slug=nc['fields']['slug'])

    default_show, _ = NewsShow.objects.get_or_create(name='Antxeta Irratia',
                                                     slug='antxeta-irratia')

    # Import news podcasts

    pk_old_to_new = {}
    for np in filter_model(objects, 'recordings.news'):
        try:
            news_podcast = NewsPodcast.objects.get(slug=np['fields']['slug'])
        except NewsPodcast.objects.DoesNotExist:
            logging.info("Importing NewsPodcast with slug {}.".format(np['fields']['slug']))
            news_podcast = NewsPodcast.objects.create(title=np['fields']['title'],
                                                      slug=np['fields']['slug'],
                                                      description=np['fields']['text'],
                                                      pub_date=make_aware(parse(np['fields']['pub_date'])),
                                                      image=np['fields']['image'],
                                                      show=default_show)
        else:
            logging.debug("Ignoring NewsPodcast with slug {}.".format(np['fields']['slug']))
        news_podcast.categories = np['fields']['categories']
        pk_old_to_new[np['pk']] = news_podcast.pk

    # Import news blobs

    news_content_type = ContentType.objects.get_for_model(NewsPodcast)
    account = Account.objects.get(name=ACCOUNT_NAME)

    for b in filter_model(objects, 'multimedia.media'):
        if all((b['fields']['content_type'] == ['recordings', 'news'],
                b['fields']['remote'] and b['fields']['remote'].startswith('http'))):
            if Blob.objects.filter(remote=b['fields']['remote']).exists():
                logging.debug("Ignoring Blob with remote {}.".format(b['fields']['remote']))
            else:
                logging.info("Importing Blob with remote {}.".format(b['fields']['remote']))
                siblings = Blob.objects.filter(content_type=news_content_type,
                                               object_id=pk_old_to_new[b['fields']['object_id']])
                position = siblings.aggregate(position=Max('position'))['position']
                position = 0 if position is None else position + 1

                Blob.objects.create(content_type=news_content_type,
                                    object_id=pk_old_to_new[b['fields']['object_id']],
                                    position=position,
                                    remote=b['fields']['remote'],
                                    account=account)


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
