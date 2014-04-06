#!/usr/bin/env python

import logging
import os
import re
import sys

from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import NewPost, WordPressPost
from flickr2wp_worker import get_set_photos, render_photos

FLICKR_SET_URL = r'([\w ]*)\nhttps://www.flickr.com/.+/photos/(?P<user>\w+)/sets/(?P<set>\d+)/'
WP_RPC_URL = os.environ.get('WP_RPC_URL', 'http://example.com/xmlrpc.php')
WP_USER = os.environ.get('WP_USER', 'user')
WP_PASS = os.environ.get('WP_PASS', 'pass')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/tmp/flickr2wordpress.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.debug('Starting processing...')

def get_user_set_from_email(raw_email):
    match = re.search(FLICKR_SET_URL, raw_email)
    if match:
        title, user_id, set_id = match.groups()
        return user_id, set_id, title
    else:
        raise Exception("Can't find user & set in email text.")

def post_to_wordpress(title, content):
    wp = Client(WP_RPC_URL, WP_USER, WP_PASS)
    post = WordPressPost()
    post.title = title
    post.content = content
    logger.debug('Sending RPC call to wordpress...')
    wp.call(NewPost(post))

def main():
    logger.info('Message received')
    content = sys.stdin.read()
    logger.debug(content)
    user_id, set_id, set_name = get_user_set_from_email(content)
    photos = get_set_photos(set_id)
    logger.debug('Rendering post content...')
    content = render_photos(photos)
    logger.debug('Creating new draft post...')
    post_to_wordpress(set_name, content)
    logger.info('Success!')


if __name__ == '__main__':
    main()

