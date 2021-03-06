#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

LOAD_CONTENT_CACHE = False

THEME = "attila"

AUTHOR = 'xiaojia'
SITENAME = 'Stay Hungry, Stay Foolish'
SITEURL = ''

PATH = 'content'
OUTPUT_PATH = "output/"
PAGE_PATHS = ["pages"]
ARTICLE_PATHS = ["articles"]
STATIC_PATHS = ["images"]

EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'},
}

PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['neighbors']

MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
		'markdown.extensions.toc':{},
    },
    'output_format': 'html5',
}


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


DIRECT_TEMPLATES = ['index', 'categories', 'authors', 'archives']

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
#SOCIAL = (('twitter', 'https://twitter.com/myprofile'),
#          ('github', 'https://github.com/XiaojiaZhang'),
#          ('facebook','https://facebook.com/myprofile'),
#          ('flickr','https://www.flickr.com/myprofile/'),
#          ('envelope','mailto:my@mail.address'))

DEFAULT_PAGINATION = 2

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

USE_FOLDER_AS_CATEGORY = True
DEFAULT_DATE = "fs"

# Theme specific settings
MENUITEMS = (('Archive', '/archives.html'), 
			 ("书评", "/category/shu-ping.html"),
			 ("杂文", "/category/za-wen.html"),
			 ("python", "/category/python.html"),
			("计算机网络", "/category/ji-suan-ji-wang-luo.html"),
			("scala", "/category/scala.html"),
)

HEADER_COVER = "images/home-bg.jpg"





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
