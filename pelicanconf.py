#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import os

AUTHOR = u'Kasper Jacobsen'
SITENAME = u'mackwerk.dk'

SITEURL = 'http://mackwerk.dk'

if os.environ.get('DEV'):
    RELATIVE_URLS = True

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'

DEFAULT_PAGINATION = 15

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

STATIC_PATHS = ['extra/CNAME', 'images']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

THEME = os.path.join(os.getcwd(), 'mackwerk.dk-theme')
