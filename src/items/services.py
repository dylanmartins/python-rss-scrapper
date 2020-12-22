
import hashlib
import logging
from datetime import datetime

from django.shortcuts import get_object_or_404

from feeds.models import Feed
from items.models import Item

logger = logging.getLogger(__name__)


class ItemsManagerService:

    def _create_md5(self, item):
        return hashlib.md5(
            str(item).encode('utf-8')
        ).hexdigest()

    def _get_item(self, item):
        return {
            'uuid': item.uuid,
            'title': item.title,
            'is_read': item.is_read,
            'created_at': item.created_at
        }

    def _convert_published_to_datetime(self, published):
        try:
            splitted_published = published.split()
            del splitted_published[-1]

            return datetime.strptime(
                ' '.join(splitted_published), '%a, %d %b %Y %H:%M:%S'
            )
        except ValueError as err:
            logger.error(
                f'Error while converting published date {published}'
            )
            return datetime.now().replace(microsecond=0)

    def _create_item_object(self, item, feed):
        published_date = self._convert_published_to_datetime(item['published'])
        return {
            'title': item['title'],
            'url': item['link'],
            'published': published_date,
            'feed': feed
        }

    def _get_filteres_items(self, item, show_all_read, show_all_unread):
        if all([show_all_read, show_all_unread]):
            return item.all()

        is_read = True if show_all_read else False
        return item.filter(is_read=is_read)

    def get_all_items_by_feed(
        self,
        uuid,
        user,
        show_all_read,
        show_all_unread
    ):
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

    def create_items_from_feed(self, items, feed):
        '''
        This method receives a list of items and a feed,
        and try to create items based on a md5 hash.
        '''
        new_items = []
        for item in items:
            item_object = self._create_item_object(item, feed)
            md5 = self._create_md5(item_object)

            if not Item.objects.filter(md5=md5).exists():
                item_object.update(md5=md5)
                new_items.append(Item(**item_object))

        return Item.objects.bulk_create(new_items)
