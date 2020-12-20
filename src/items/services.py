import json

from django.core import serializers
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

from feeds.models import Feed
from items.models import Item


class ItemsManagerService:

    def _get_item(self, item):
        return {
            'uuid': item.uuid,
            'title': item.title,
            'is_read': item.is_read,
            'created_at': item.created_at,
            'updated_at': item.updated_at
        }

    def _get_filteres_items(self, item, show_all_read, show_all_unread):
        if all([show_all_read, show_all_unread]):
            return item.all()

        is_read = True if show_all_read else False
        return item.filter(is_read=is_read)

    def get_all_items_by_feed(self, uuid, user, show_all_read, show_all_unread):
        '''
        This method returns all items from a specific feed checking the user.
        You can filter using a querystring, for example:
            - http://localhost:8000/feeds/?show_all_read=true
            - http://localhost:8000/feeds/?show_all_unread=true
        '''
        feed = get_object_or_404(Feed, uuid=uuid, follower=user)

        if any([show_all_read, show_all_unread]):
            items = self._get_filteres_items(
                feed.items,
                show_all_read,
                show_all_unread
            )
        else:
            items = feed.items.all()
            
        return [
            self._get_item(item)
            for item in items
        ]

    def get_item_and_set_is_read(self, uuid, user):
        '''
        This method gets a specific item, sets it as read, and return its data.
        '''
        item = get_object_or_404(Item, uuid=uuid, feed__follower=user)
        item.is_read = True
        item.save()
        return self._get_item(item)
