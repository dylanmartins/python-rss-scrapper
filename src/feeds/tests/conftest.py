import pytest

from feeds.models import Feed


@pytest.fixture
def cleanup():
    yield
    # This is executed when the test using the fixture is done
    Feed.objects.all().delete()


@pytest.fixture
def save_feeds(
    normal_user_a,
    normal_user_b,
    cleanup
):
    feed_data = {
        'title': 'Test feed',
        'url': 'http://www.nu.nl/rss/Algemeen',
        'follower': normal_user_a
    }
    Feed.objects.create(**feed_data)

    feed_data['follower'] = normal_user_b
    Feed.objects.create(**feed_data)
