#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

LOAD_CONTENT_CACHE = False

THEME = "attlia"

AUTHOR = 'xiaojia'
SITENAME = 'Stay Hungry, Stay Foolish'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = "output/"
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["articles"]
STATIC_PATHS = ["images"]

TIMEZONE = 'UTC'

DEFAULT_LANG = 'en'
SUMMARY_MAX_LENGTH = 100
DATE_FORMATS = {'en': "%d/%m/%Y", 'zh': "%d/%m/%y"}

DISPLAY_PAGES_ON_MENU = True
# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
#SOCIAL = (("github", 'https://github.com/XiaojiaZhang'),
#		  ("facebook", "https://github.com/XiaojiaZhang"),
#		  ('You can add links in your config file', '#'),
#          ('Another social link', '#'),)
SOCIAL = (('twitter', 'https://twitter.com/myprofile'),
          ('github', 'https://github.com/XiaojiaZhang'),
          ('facebook','https://facebook.com/myprofile'),
          ('flickr','https://www.flickr.com/myprofile/'),
          ('envelope','mailto:my@mail.address'))

DEFAULT_PAGINATION = 2

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

USE_FOLDER_AS_CATEGORY = True
DEFAULT_DATE = "fs"

# Theme specific settings
MENUITEMS = (('Archive', 'archives.html'),
			 ("About me", "pages/about-me.html"), )

HEADER_COVER = "images/home-bg.jpg"
GITHUB_URL = "https://github.com/XiaojiaZhang"






HEADER_COVERS_BY_TAG = {'python': 'images/python_logo.svg',
						'linux': "images/linux_logo.png"}


HEADER_COLOR = "white"
AUTHORS_BIO = {
	"xiaojia": {
		"name": "xiaojia",
    	"cover": "https://casper.ghost.org/v1.0.0/images/team.jpg",
		"image": "images/touxiang.jpeg",
		"github": "XiaojiaZhang",
		"location": "Beijing",
		"bio": "北京交通大学交通运输规划与管理专业"
	}
}
