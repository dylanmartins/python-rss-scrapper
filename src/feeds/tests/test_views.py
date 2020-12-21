import uuid

import pytest
from django.urls import reverse_lazy

from feeds.models import Feed


@pytest.mark.django_db
class TestFeedsView:

    def test_get_view_should_return_all_user_feeds(
        self,
        api_client,
        save_feeds
    ):
        count = Feed.objects.all().count()
        url = reverse_lazy('feeds:index')
        response = api_client.get(url)
        json_content = response.json()

        assert response.status_code == 200
        assert len(json_content['data']) == 1
        assert json_content['data'][0]['url'] == 'http://www.nu.nl/rss/Algemeen'  # noqa
        assert json_content['data'][0]['title'] == 'Test feed'
        assert count == 2

    def test_get_view_without_feeds_should_not_return_all_user_feeds(
        self,
        api_client
    ):
        count = Feed.objects.all().count()
        url = reverse_lazy('feeds:index')
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.json() == {
            'data': []
        }
        assert count == 0


@pytest.mark.django_db
class TestCreateFeedsView:

    def test_post_view_should_create_new_feed(
        self,
        api_client,
        valid_feed_data
    ):
        assert Feed.objects.all().count() == 0

        url = reverse_lazy('feeds:create')
        response = api_client.post(
            url,
            data=valid_feed_data
        )
        assert response.status_code == 201
        assert Feed.objects.all().count() == 1

    def test_post_view_should_return_conflict_if_feed_exists(
        self,
        api_client,
        save_feeds,
        valid_feed_data
    ):
        assert Feed.objects.all().count() == 2

        url = reverse_lazy('feeds:create')
        response = api_client.post(
            url,
            data=valid_feed_data
        )
        assert response.status_code == 409
        assert Feed.objects.all().count() == 2


@pytest.mark.django_db
class TestDeleteFeedsView:

    def test_delete_view_should_delete_feed_if_exists(
        self,
        api_client,
        save_feeds,
        valid_feed_a,
        valid_feed_data
    ):
        assert Feed.objects.all().count() == 2
        url = reverse_lazy(
            'feeds:delete',
            kwargs={
                'uuid': str(valid_feed_a.uuid)
            }
        )
        response = api_client.delete(url)

        assert response.status_code == 204
        assert Feed.objects.all().count() == 1

    def test_delete_view_invalid_uuid_should_do_nothing(
        self,
        api_client,
        save_feeds,
        valid_feed_data
    ):
        assert Feed.objects.all().count() == 2
        url = reverse_lazy(
            'feeds:delete',
            kwargs={
                'uuid': str(uuid.uuid4())
            }
        )
        response = api_client.delete(url)

        assert response.status_code == 400
        assert Feed.objects.all().count() == 2
