from django.forms.models import model_to_dict

from feeds.models import Feed


class FeedsManagerService:

    def get_all_feeds_by_user(self, user):
        all_feeds = Feed.objects.filter(
            follower=user
        )
        return [
            model_to_dict(feed, fields=['title', 'url'])
            for feed in all_feeds
        ]
