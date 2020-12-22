from unittest import mock

import pytest

from celery.exceptions import Retry
from feeds.models import Feed
from feeds.tasks import get_items_by_feed, update_all_feed_items
from items.models import Item


@pytest.mark.django_db
class TestUpdateAllFeedItems:

    @pytest.fixture(autouse=True)
    def settings(self, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True

        return settings

    def test_update_all_feed_items_should_update_all_items(
        self,
        save_feeds,
        valid_items
    ):
        assert Feed.objects.all().count() == 2
        assert Item.objects.all().count() == 0

        with mock.patch(
            'feeds.tasks.scrapper.scrappy'
        ) as mock_scrapper:
            mock_scrapper.return_value = valid_items
            update_all_feed_items.delay()

        assert Item.objects.all().count() == 2

    def test_update_all_feed_items_should_retry_and_raise_if_error(
        self,
        save_feeds,
        valid_items
    ):
        assert Feed.objects.all().count() == 2
        assert Item.objects.all().count() == 0

        with mock.patch(
            'feeds.tasks.scrapper.scrappy'
        ) as mock_scrapper:
            mock_scrapper.return_value = valid_items
            mock_scrapper.side_effect = Exception
            with pytest.raises(Retry):
                update_all_feed_items()

        assert Item.objects.all().count() == 0


@pytest.mark.django_db
class TestGetItemsByFeed:

    @pytest.fixture(autouse=True)
    def settings(self, settings):
        settings.CELERY_TASK_ALWAYS_EAGER = True

        return settings

    def test_get_items_by_feed_should_update_all_items_from_feed(
        self,
        save_feeds,
        valid_feed_a,
        valid_items
    ):
        uuid_feed = str(valid_feed_a.uuid)
        assert Feed.objects.filter(uuid=uuid_feed).count() == 1
        assert Item.objects.all().count() == 0

        with mock.patch(
            'feeds.tasks.scrapper.scrappy'
        ) as mock_scrapper:
            mock_scrapper.return_value = valid_items
            get_items_by_feed.delay(uuid_feed=uuid_feed)

        assert Item.objects.all().count() == 1

    def test_get_items_by_feed_should_retry_and_raise_if_error(
        self,
        save_feeds,
        valid_feed_a,
        valid_items
    ):
        uuid_feed = str(valid_feed_a.uuid)
        assert Feed.objects.filter(uuid=uuid_feed).count() == 1
        assert Item.objects.all().count() == 0

        with mock.patch(
            'feeds.tasks.scrapper.scrappy'
        ) as mock_scrapper:
            mock_scrapper.return_value = valid_items
            mock_scrapper.side_effect = Exception
            with pytest.raises(Retry):
                get_items_by_feed(uuid_feed=uuid_feed)

        assert Item.objects.all().count() == 0
