import json

from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from feeds.models import Feed


class ItemsManagerService:

    def get_all_items_by_feed(self, uuid, user):
        '''
        This method returns all items from a specific feed checking the user.
        '''
        feed = get_object_or_404(Feed, uuid=uuid, follower=user)
        items = feed.items.all()
        return [
            {
                'uuid': item.uuid,
                'title': item.title,
                'is_read': item.is_read,
                'created_at': item.created_at,
                'updated_at': item.updated_at
            }
            for item in items
        ]
