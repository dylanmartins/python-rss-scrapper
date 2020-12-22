from datetime import datetime

import pytest

from items.models import Item
from items.services import ItemsManagerService


@pytest.mark.django_db
class TestItemsManagerService:

    @pytest.fixture
    def manager(self):
        return ItemsManagerService()

    def test_create_item_object_should_create_valid_md5(
        self,
        manager,
        valid_feed_a
    ):
        item = {
            'feed': 'd459d450b0aba02d4470466a5464bfb2',
            'md5': 'd459d450b0aba02d4470466a5464bfb2',
            'published': datetime(2020, 12, 21, 20, 38),
            'title': "'Among Us is met 500 miljoen actieve spelers meest populaire game ooit'",  # noqa
            'url': 'https://tweakers.net/nieuws/176016/among-us-is-met-500-miljoen-actieve-spelers-meest-populaire-game-ooit.html'  # noqa
        }
        result = manager._create_md5(item)
        assert result == '3b347eca0ad732b079b2033adcf6b3de'

    def test_create_items_from_feed_should_create_items_in_db(
        self,
        manager,
        valid_items,
        save_feeds,
        valid_feed_a
    ):
        assert Item.objects.all().count() == 0

        manager.create_items_from_feed(valid_items, valid_feed_a)

        assert Item.objects.all().count() == 1

    def test_create_items_from_feed_should_not_create_items_in_db_if_md5_exists(  # noqa
        self,
        manager,
        save_feeds,
        valid_items,
        valid_feed_a
    ):
        manager.create_items_from_feed(valid_items, valid_feed_a)

        assert Item.objects.all().count() == 1

        manager.create_items_from_feed(valid_items, valid_feed_a)

        assert Item.objects.all().count() == 1
