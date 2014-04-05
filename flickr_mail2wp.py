#!/usr/bin/env python

import logging
import re
import sys

from flickr2wp_worker import get_set_photos, render_photos

FLICKR_SET_URL = r'https://www.flickr.com/.+/photos/(?P<user>\w+)/sets/(?P<set>\d+)/'

logging.basicConfig(filename='/tmp/flickr2wordpress.log',level=logging.DEBUG)

def get_user_set_from_email(raw_email):
    match = re.search(FLICKR_SET_URL, raw_email)
    if match:
        user_id, set_id = match.groups()
        return user_id, set_id
    else:
        raise Exception("Can't find user & set in email text.")

def main():
    logging.debug('Message received')
    content = sys.stdin.read()
    user_id, set_id = get_user_set_from_email(content)
    photos = get_set_photos(set_id)
    logging.debug('Creating new draft post.')
    logging.debug(render_photos(photos))
    # create_new_post()


logging.debug('Starting processing...')
if __name__ == '__main__':
    main()

