import logging
import uuid

from celery import shared_task

from feeds.models import Feed
from items.models import Item

logger = logging.getLogger(__name__)


@shared_task
def update_all_feed_items():

    logger.info('Starting task update_all_feed_items')

    all_feeds = Feed.objects.all()
    for feed in all_feeds:
        item = Item(
            title=f'Test random {str(uuid.uuid4())}',
            feed=feed
        )
        item.save()

    logger.info('Finished task update_all_feed_items')


@shared_task
def get_items_by_feed(uuid_feed):
    logger.info('Starting task get_items_by_feed')

    try:
        feed = Feed.objects.get(uuid=uuid_feed)
        item = Item(
            title=f'Test random {str(uuid.uuid4())}',
            feed=feed
        )
        item.save()
    except Exception as err:
        logger.error(
            'Error on task update_all_feed_items using '
            f'UUID {uuid_feed}. Error:{err}'
        )
        return

    logger.info('Finished task get_items_by_feed')
