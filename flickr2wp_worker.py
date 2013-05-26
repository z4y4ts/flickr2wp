import re
import sys

import flickrapi
from jinja2 import Template

API_KEY = '7fa8d2c3af054ab89adea2bd0220ae66'
SIZE = 'Original'


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
                                                  extras='url_o')
                             .getiterator('photo'))  # Python 2.6 compatibility
    for photo in photoset_photos:
        yield {'title': photo.attrib.get('title'),
               'alt': photo.attrib.get('title'),
               'href': photo.attrib.get('url_o')}


def render_photos(photos):
    with open('photoset-template.html', 'r') as f:
        template = Template(f.read())
    return template.render(photos=photos)

if __name__ == '__main__':
    main()
