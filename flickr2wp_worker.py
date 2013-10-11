import os
import re
import sys

import flickrapi
from jinja2 import Template

API_KEY = '7fa8d2c3af054ab89adea2bd0220ae66'
SIZES = {'Square 75': 'url_s',
         'Square 150': 'url_q',
         'Thumbnail': 'url_t',
         'Small 240': 'url_s',
         'Small 320': 'url_n',
         'Medium 500': 'url_m',
         'Medium 640': 'url_z',
         'Medium 800': 'url_c',
         'Large 1024': 'url_l',
         'Large 1600': 'url_h',
         'Original': 'url_o'}


def main():
    inp = sys.stdin.read()
    sys.stderr.write(inp)

    set_id = find_set_id(inp)
    photos = get_set_photos(set_id)
    sys.stdout.write(render_photos(photos))


def find_set_id(text):
    m = re.search('http://www.flickr.com/photos/(?P<user>[\w@]+)/sets/(?P<set_id>\d+)/', text, re.M)
    return m.groupdict().get('set_id')


def get_set_photos(set_id):
    """
    Returns {'photo_title': 'title', 'href': 'http://...'} sequence.
    """
    flickr = flickrapi.FlickrAPI(API_KEY)
    photoset_photos = (flickr.photosets_getPhotos(api_key=API_KEY,
                                                  photoset_id=set_id,
                                                  extras=(SIZES['Medium 640'], SIZES['Original']))
                             .getiterator('photo'))  # Python 2.6 compatibility
    # for photo in sorted(photoset_photos, key=lambda p: p.attrig.get('title')):
    for photo in photoset_photos:
        photo_url = photo.attrib.get(SIZES['Medium 640'])
        if not photo_url:
            photo_url = photo.attrib.get(SIZES['Original'])
        yield {'title': photo.attrib.get('title').replace('-', ' '),
               'alt': photo.attrib.get('title').replace('-', ' '),
               'href': photo_url}


def render_photos(photos):
    with open('photoset-template.html', 'r') as f:
        template = Template(f.read())
    return template.render(photos=photos)

if __name__ == '__main__':
    main()
