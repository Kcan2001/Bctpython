# Please note, we use not official python-instagram, because it's not actively maintained anymore
# We use https://github.com/shackra/python-instagram/ instead
from instagram.client import InstagramAPI

from django.conf import settings


INSTAGRAM_ACCESS_TOKEN = settings.INSTAGRAM_ACCESS_TOKEN
INSTAGRAM_CLIENT_ID = settings.INSTAGRAM_CLIENT_ID
INSTAGRAM_CLIENT_SECRET = settings.INSTAGRAM_CLIENT_SECRET


class GetUserMedia(object):

    # You can set how many photos will be shown in settings file. Can be only 1-20 photos.
    # We set default to 20
    @staticmethod
    def recent_media(count):
        api = InstagramAPI(access_token=INSTAGRAM_ACCESS_TOKEN, client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET)

        recent_media, next_ = api.user_recent_media(count=count)

        photos = []

        for media in recent_media:
            if media.type != 'video':
                photos.append({
                    'link': media.link,
                    'image': media.images['standard_resolution'].url,
                    'likes': media.like_count,
                    'comments': media.comment_count
                })

        return photos
