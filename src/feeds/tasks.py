import logging
import uuid

from celery import shared_task
from contrib.scrappers import RssScrapper
from feeds.models import Feed
from items.services import ItemsManagerService

logger = logging.getLogger(__name__)
scrapper = RssScrapper()
items_manager = ItemsManagerService()


@shared_task
def update_all_feed_items():
    logger.info('Starting task update_all_feed_items')

    all_feeds = Feed.objects.all()
    for feed in all_feeds:
        items = scrapper.scrappy(feed.url)
        items_manager.create_items_from_feed(items, feed)

    logger.info('Finished task update_all_feed_items')


@shared_task
def get_items_by_feed(uuid_feed):
    logger.info('Starting task get_items_by_feed')

    try:
        feed = Feed.objects.get(uuid=uuid_feed)
        items = scrapper.scrappy(feed.url)
        items_manager.create_items_from_feed(items, feed)
    except Exception as err:
        logger.error(
            'Error on task update_all_feed_items using '
            f'UUID:{uuid_feed}. Error:{err}'
        )
        return

    logger.info('Finished task get_items_by_feed')
