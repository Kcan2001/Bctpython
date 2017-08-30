# Please note, we use not official python-instagram, because it's not actively maintained anymore
# We use https://github.com/shackra/python-instagram/ instead
from instagram.client import InstagramAPI

# Access token, client id and client secret for your instagram account
Instagram_ACCESS_TOKEN = "1970669399.500378d.00ac5756029c4de58a8f57e12ee2c3c1"
Instagram_CLIENT_ID = "500378dd00a34eaea47f257721c7e4c6"
Instagram_CLIENT_SECRET = "3db3204916074515aa19d4b54a88a88b"


class GetUserMedia(object):

    # From views in count we determine how many photos will show. Can be only 1-20 photos. We set default to 18.
    def recent_media(count):
        api = InstagramAPI(access_token=Instagram_ACCESS_TOKEN, client_id=Instagram_CLIENT_ID,
                           client_secret=Instagram_CLIENT_SECRET)

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
