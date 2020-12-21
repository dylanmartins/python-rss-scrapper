
from django.shortcuts import get_object_or_404

from feeds.models import Feed
from feeds.tasks import get_items_by_feed


class FeedsManagerService:

    def get_all_feeds_by_user(self, user):
        '''
        This method returns all feeds from a specific user.
        '''
        all_feeds = Feed.objects.filter(follower=user)
        return [
            {
                'uuid': feed.uuid,
                'title': feed.title,
                'url': feed.url,
                'created_at': feed.created_at,
                'updated_at': feed.updated_at
            }
            for feed in all_feeds
        ]

    def get_or_create_feed(self, data):
        '''
        This method checks if the feed already exists, if don't its created.
        '''
        _, created = Feed.objects.get_or_create(
            url=data['url'],
            follower=data['follower'],
            defaults={'title': data['title']},
        )
        return created

    def delete_feed(self, uuid, user):
        '''
        This method deletes a feed using a UUID, if the feed
        exists return 1 else 0.
        '''
        deleted, _ = Feed.objects.filter(uuid=uuid, follower=user).delete()
        return deleted

    def update_feed(self, uuid, user):
        '''
        This method updates feed items using a UUID from a feed, if the feed
        exists this methos calls an async task.
        '''
        feed = get_object_or_404(Feed, uuid=uuid, follower=user)
        get_items_by_feed.delay(str(feed.uuid))
        return True
