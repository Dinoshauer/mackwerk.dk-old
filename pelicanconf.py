#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Kasper Jacobsen'
SITENAME = u'mackwerk.dk'
SITEURL = ''

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'

DEFAULT_PAGINATION = 15

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

STATIC_PATHS = ['extra/CNAME']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
}

THEME = "/home/k/git/mackwerk.dk/mackwerk.dk-theme"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
