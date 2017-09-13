# Please note, we use not official python-instagram, because it's not actively maintained anymore
# We use https://github.com/shackra/python-instagram/ instead
from django.conf import settings
from instagram.client import InstagramAPI

# Access token, client id and client secret for your instagram account
INSTAGRAM_ACCESS_TOKEN = settings.INSTAGRAM_ACCESS_TOKEN
INSTAGRAM_CLIENT_ID = settings.INSTAGRAM_CLIENT_ID
INSTAGRAM_CLIENT_SECRET = settings.INSTAGRAM_CLIENT_SECRET


class GetUserMedia(object):

    # From views in count we determine how many photos will show. Can be only 1-20 photos.
    # We set default to 20 in views.py.
    @staticmethod
    def recent_media(count):
        api = InstagramAPI(access_token=INSTAGRAM_ACCESS_TOKEN, client_id=INSTAGRAM_CLIENT_ID,
                           client_secret=INSTAGRAM_CLIENT_SECRET)

        recent_media, next_ = api.user_recent_media(count=count)

        # Will make our list blank
        photos = list()

        for media in recent_media:

            # Create dict for every instance from user's instagram
            recent_photos = dict()
            # Will show only images, without video, cuz we can't control their responsiveness in template
            if media.type == 'video':
                pass
            else:
                recent_photos['link'] = media.link
                recent_photos['image'] = media.images['standard_resolution'].url
                recent_photos['likes'] = media.like_count
                recent_photos['comments'] = media.comment_count
                photos.append(recent_photos)
        return photos
