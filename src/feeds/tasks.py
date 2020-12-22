import logging

from celery import shared_task
from django.conf import settings

from contrib.scrappers import RssScrapper
from feeds.models import Feed
from items.services import ItemsManagerService

logger = logging.getLogger(__name__)
scrapper = RssScrapper()
items_manager = ItemsManagerService()


@shared_task(
    bind=True,
    max_retries=settings.CELERY_MAX_RETRIES,
    default_retry_delay=settings.CELERY_RETRY_DELAY['update_all_feed_items'],
)
def update_all_feed_items(self):
    logger.info('Starting task update_all_feed_items')

    try:
        all_feeds = Feed.objects.all()
        for feed in all_feeds:
            items = scrapper.scrappy(feed.url)
            items_manager.create_items_from_feed(items, feed)
    except Exception as err:
        logger.error(f'Error on task update_all_feed_items using Error:{err}')
        try:
            raise self.retry()
        except self.MaxRetriesExceededError as err:
            logger.critical('Max retries to update_all_feed_items reached')
            raise err

    logger.info('Finished task update_all_feed_items')


@shared_task(
    bind=True,
    max_retries=settings.CELERY_MAX_RETRIES,
    default_retry_delay=settings.CELERY_RETRY_DELAY['get_items_by_feed'],
)
def get_items_by_feed(self, uuid_feed):
    logger.info('Starting task get_items_by_feed')

    try:
        feed = Feed.objects.get(uuid=uuid_feed)
        items = scrapper.scrappy(feed.url)
        items_manager.create_items_from_feed(items, feed)
    except Exception as err:
        logger.error(
            'Error on task get_items_by_feed using '
            f'UUID:{uuid_feed}. Error:{err}'
        )
        try:
            raise self.retry()
        except self.MaxRetriesExceededError:
            logger.critical('Max retries to get_items_by_feed reached')

    logger.info('Finished task get_items_by_feed')
