from datetime import datetime
from unittest.mock import patch

import pytest
import requests
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from feeds.models import Feed
from items.models import Item


@pytest.fixture
def normal_user_a():
    return User.objects.create_user(
        username='userA',
        email='userA@foo.com',
        password='pass'
    )


@pytest.fixture
def normal_user_b():
    return User.objects.create_user(
        username='userB',
        email='userB@foo.com',
        password='pass'
    )


@pytest.fixture
def api_client(normal_user_a):
    client = APIClient()
    refresh = RefreshToken.for_user(normal_user_a)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


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
def valid_feed_a(valid_feed_data, normal_user_a):
    valid_feed_data['follower'] = normal_user_a
    return Feed.objects.create(**valid_feed_data)


@pytest.fixture
def valid_feed_b(valid_feed_data, normal_user_b):
    valid_feed_data['follower'] = normal_user_b
    return Feed.objects.create(**valid_feed_data)


@pytest.fixture
def save_feeds(
    valid_feed_a,
    valid_feed_b,
    cleanup
):
    return


@pytest.fixture
def valid_items_a(
    save_feeds,
    valid_feed_a,
    cleanup
):
    return Item.objects.create(
        title='Test item',
        feed=valid_feed_a
    )


@pytest.fixture
def valid_items_b(
    save_feeds,
    valid_feed_b,
    cleanup
):
    return Item.objects.create(
        title='Test item B',
        feed=valid_feed_b
    )


@pytest.fixture
def save_items(valid_items_a, valid_items_b, cleanup):
    return


@pytest.fixture
def patch_requests_get():
    return patch.object(requests, 'get')
