#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = u'Jesús Torres'
SITENAME = u'Sistema de Videovigilancia from Scratch'
SITEURL = 'http://ull-etsii-sistemas-operativos.github.io/videovigilancia-blog'

RELATIVE_URLS = True

TIMEZONE = 'Atlantic/Canary'

DEFAULT_LANG = u'es'

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})_(?P<slug>.*)'
SUMMARY_MAX_LENGTH = 50

GOOGLE_CUSTOM_SEARCH_SIDEBAR = '013894742475483232300:q2-5a1zlira'
DISQUS_SITENAME = 'sistema-de-videovigilancia-from-scratch'

# Plugins
PLUGINS = ['plugins.sitemap']

# Sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'weekly',
        'indexes': 'weekly',
        'pages': 'yearly'
    }
}

# Feeds
FEED_DOMAIN = SITEURL
FEED_ATOM='feeds/atom.xml'
FEED_RSS='feeds/rss.xml'

# Blogroll
LINKS =  ()

# Author profiles
PROFILES = {u'Jesús Torres': (
            ('jmtorres', 'http://plus.google.com/u/0/113130190517682041034'),
            ('@susotorres', 'http://twitter.com/susotorres'),)}

# Social widget
SOCIAL = (('github', 'http://github.com/ull-etsii-sistemas-operativos/'),
          ('google+', 'http://plus.google.com/u/0/communities/112085352199958768374'),
          ('flattr', 'http://flattr.com/thing/1171169/Sistema-de-videovigilancia-from-scratch'),
          ('atom', FEED_DOMAIN + '/' + FEED_ATOM),
          ('rss', FEED_DOMAIN + '/' + FEED_RSS),)

DEFAULT_PAGINATION = 3

# Theme
THEME = u'themes/tuxlite_tbs'
