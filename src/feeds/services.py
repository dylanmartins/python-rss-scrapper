import json
from django.core import serializers
from django.forms.models import model_to_dict

from feeds.models import Feed


class FeedsManagerService:

    def get_all_feeds_by_user(self, user):
        '''
        This method returns title and url of all feeds from a specific user.
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

    def delete_feed(self, uuid):
        '''
        This method deletes a feed using a UUID, if the feed 
        exists return 1 else 0.
        '''
        deleted, _= Feed.objects.filter(uuid=uuid).delete()
        return deleted
