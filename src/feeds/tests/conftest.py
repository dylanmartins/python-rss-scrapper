import pytest

from feeds.models import Feed


@pytest.fixture
def cleanup():
    yield
    # This is executed when the test using the fixture is done
    Feed.objects.all().delete()


@pytest.fixture
def valid_feed_data():
    return {
        'title': 'Test feed',
        'url': 'http://www.nu.nl/rss/Algemeen',
        'created_at': '2020-12-19T20:55:12.163Z',
        'updated_at': '2020-12-19T20:55:12.163Z',
    }


@pytest.fixture
def save_feeds(
    normal_user_a,
    normal_user_b,
    valid_feed_data,
    cleanup
):
    valid_feed_data['follower'] = normal_user_a
    Feed.objects.create(**valid_feed_data)

    valid_feed_data['follower'] = normal_user_b
    return Feed.objects.create(**valid_feed_data)
