import uuid

import pytest
from django.urls import reverse_lazy

from items.models import Item


@pytest.mark.django_db
class TestItemsFeedView:

    def test_get_view_should_return_all_items_by_feed(
        self,
        api_client,
        save_feeds,
        save_items,
        valid_feed_a
    ):
        assert Item.objects.all().count() == 2

        url = reverse_lazy(
            'items:index',
            kwargs={'uuid_feed': str(valid_feed_a.uuid)}
        )
        response = api_client.get(url)
        json_content = response.json()

        assert response.status_code == 200
        assert len(json_content['data']) == 1
        assert json_content['data'][0]['title'] == 'Test item'
        assert json_content['data'][0]['is_read'] is False

    def test_get_view_should_return_all_unread_items_by_feed(
        self,
        api_client,
        save_feeds,
        save_items,
        valid_feed_a
    ):
        assert Item.objects.all().count() == 2

        url = reverse_lazy(
            'items:index',
            kwargs={'uuid_feed': str(valid_feed_a.uuid)}
        )
        response = api_client.get(f'{url}?show_all_unread=true')
        json_content = response.json()

        assert response.status_code == 200
        assert len(json_content['data']) == 1
        assert json_content['data'][0]['title'] == 'Test item'
        assert json_content['data'][0]['is_read'] is False

    def test_get_view_should_return_all_read_items_by_feed(
        self,
        api_client,
        save_feeds,
        save_items,
        valid_feed_a
    ):
        assert Item.objects.all().count() == 2

        url = reverse_lazy(
            'items:index',
            kwargs={'uuid_feed': str(valid_feed_a.uuid)}
        )
        response = api_client.get(f'{url}?show_all_read=true')
        json_content = response.json()

        assert response.status_code == 200
        assert len(json_content['data']) == 0

    def test_get_view_should_return_all_read_and_unread_items_by_feed(
        self,
        api_client,
        save_feeds,
        save_items,
        valid_feed_a
    ):
        assert Item.objects.all().count() == 2

        url = reverse_lazy(
            'items:index',
            kwargs={'uuid_feed': str(valid_feed_a.uuid)}
        )
        response = api_client.get(
            f'{url}?show_all_read=true&show_all_unread=true'
        )
        json_content = response.json()

        assert response.status_code == 200
        assert len(json_content['data']) == 1
        assert json_content['data'][0]['title'] == 'Test item'
        assert json_content['data'][0]['is_read'] is False

    def test_get_view_should_not_return_all_items_with_wrong_user(
        self,
        api_client,
        save_feeds,
        save_items,
        valid_feed_b
    ):
        assert Item.objects.all().count() == 2

        url = reverse_lazy(
            'items:index',
            kwargs={'uuid_feed': str(valid_feed_b.uuid)}
        )
        response = api_client.get(url)

        assert response.status_code == 404


@pytest.mark.django_db
class TestReadItemView:

    def test_get_view_should_return_item_and_set_is_read_true(
        self,
        api_client,
        save_feeds,
        save_items,
        valid_items_a
    ):
        item_uuid = str(valid_items_a.uuid)

        item = Item.objects.get(uuid=item_uuid)
        url = reverse_lazy(
            'items:read',
            kwargs={'uuid_item': item_uuid}
        )
        response = api_client.get(url)
        json_content = response.json()

        unread_item = Item.objects.get(uuid=item_uuid)

        assert response.status_code == 200
        assert json_content['data']['title'] == item.title
        assert json_content['data']['uuid'] == str(item.uuid)
        assert json_content['data']['is_read'] != item.is_read
        assert unread_item.is_read is True

    def test_get_view_should_not_return_item_and_set_is_read_true_if_invalid_uuid(  # noqa
        self,
        api_client,
        save_feeds,
    ):
        url = reverse_lazy(
            'items:read',
            kwargs={'uuid_item': str(uuid.uuid4())}
        )
        response = api_client.get(url)
        assert response.status_code == 404
