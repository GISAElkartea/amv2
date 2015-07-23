Important factors
=================

Erreproduktorea
---------------

- playlistak
- playlista jaitsi
- audioak gehitu, mugitu ahal izan, etb
- konpartitu (podcastaren helbidea)
- streamingarekin integrazioa

Kontu pertsonalak
-----------------

- gogoko irratsaioak
- feed pertsonalizatua
- *sartutako azken alditik zer da berria*
- playlistak

Nabigazioa
----------

- bilatzaile hobea
- irratsaioaetara errazago sartu

Portada
-------

- azkeneko 5ak beharrean, atzotik berria dena
- portada eta menu eraikitzailea?

Archive.org
-----------

- igoera asinkronoak, queuea igoera guztiekin

```
ARCHIVE.ORG TEST ACCOUNT
username: archive.org-test
password: archive.org-test
access key: VSh9SgRkxTYIaZUs
secret key: GsQjQ6KLtx63Sktr
```


Bestelakoak
-----------

- lizentzia argiagoak


Architecture
============

Layout
------

![Design](structure.png)

- shows:
  - AbstractProducer
  - AbstractCategory
  - AbstractShow
  - AbstractPodcast
- news:
  - NewsShow
  - NewsCategory
  - NewsPodcast
- radio
  - RadioProducer
  - RadioCategory
  - RadioShow
  - RadioPodcast
- projects
  - ProjectProducer
  - ProjectShow
  - ProjectPodcast
- blobs
  - Blob
  - BlobUpload
- playlists
- favourites
- events
- archives
- schedule
  - Label
  - Broadcast
- pages
- widgets

Design decisions
----------------

### No nested categories

They do not use them currently.

- NewsShows do not need to be categorized.
- RadioShows can be categorized in RadioCategories and RadioProducers.
- ProjectShows can be categorized in ProjectProcuers.

### No embeded multimedia models

If they want to use some external embed, they can use the description text.

### Multiple audios per podcast

They use this feature nowadays. It's true that it makes it somewhat more
difficult to manage the playlist buttons but this can be solved by:

- making the add button add all the audios of the podcast to the playlist.
- making the play button play all the adios of the podcast.
- making the share button share the podcast link.

### Only RadioShows have the "featured" boolean


User views
----------

- welcome page
- frontpage
- user frontpage
- news
    - newspodcast_list: filtered by NewsShow and NewsCategory
    - newspodcast_detail
- radio
    - radioshow_list: filtered by RadioProducer and RadioCategory
    - radiopodcast_list
    - radiopodcast_detail
- projects
    - projectproducer_list
    - projectshow_detail
- favourites
    - favourite_list
    - create_favourite
    - delete_favourite
- playlists
- settings
- archive
- events
    - event_list
    - event_detail
- schedule
    - broadcast_list
