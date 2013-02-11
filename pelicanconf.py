#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Jesús Torres'
SITENAME = u'Sistema de Videovigilancia from Scratch'
SITEURL = 'http://ull-etsii-sistemas-operativos.github.com/videovigilancia-blog'

TIMEZONE = 'Atlantic/Canary'

DEFAULT_LANG = u'es'

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
SUMMARY_MAX_LENGTH = 100

# Feeds
FEED_DOMAIN = SITEURL
FEED_ATOM='feeds/atom.xml'
FEED_RSS='feeds/rss.xml'

# Blogroll
LINKS =  ()

# Social widget
SOCIAL = (('github', 'http://github.com/ull-etsii-sistemas-operativos/'),
          ('google+', 'http://plus.google.com/u/0/communities/112085352199958768374'),
          ('atom', FEED_DOMAIN + '/' + FEED_ATOM),
          ('rss', FEED_DOMAIN + '/' + FEED_RSS),)

DEFAULT_PAGINATION = 5

# Theme
THEME = u'themes/tuxlite_tbs'

# Google
GOOGLE_CUSTOM_SEARCH_SIDEBAR = '013894742475483232300:q2-5a1zlira'
GOOGLE_API_KEY = 'AIzaSyClPfZd7RRcX9e3eYiOLV__FyRO9RmJzmg'