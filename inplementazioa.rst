==============
Implementation
==============

Radio
=====

Structure
---------

    class Category:
        name
        related = m2m Category

    class Show:
        abstract = True
        categories = m2m Category
        tags = m2m
        ...

    class Podcast
        abstract = True
        tags = m2m
        file
        license
        title
        description
        embed code

        def upload
        def is_uploaded
        def get_embed_code
        def sync

    class NewsShow(Show):
        pass

    class RadioShow(Show):
        pass

    class Project(Show):
        pass

    class NewsPodcast(Podcast):
        show = NewsShow

    class RadioPodcast(Podcast):
        show = RadioShow

    class ProjectPodcast(Podcast):
        show = Project

    class Playlist:
        user = User
        title
        order = PodcastOrder
        # otherwise, try many2many through podcast order

    class PodcastOrder:
        podcast_content_type = ContentType
        podcast_id = PositiveIntegerField
        podcast = podcast_content_type, podcast_id
        position = PositionField (django-positions)

    class UserPreferences:
        favorite_radio_shows = RadioShow
        favorite_news_shows = NewsShow

    class User:
        login with only email and pass


API
---

Playlists
~~~~~~~~~

- user's playlist list
- podcast list for playlist
- append podcast to playlist
- reorder playlist
- delete podcast in playlist
- delete playlist

Shows
~~~~~

- get user news shows
- get user radio shows
- get news list
- get radioshow list
- get project list
- get podcast details
- get podcasts for show after certain date
- get podcasts after certain date
- get shows for certain category
- get category list

Archive sync
------------

- get embed code
- get file URL
- async, queue in admin


Agenda
======

- more advanced recurrence handling etc.

Widgets
=======

Banners
=======

Static pages
============

Programming
===========
