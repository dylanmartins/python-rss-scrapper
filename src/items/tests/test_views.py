import pytest
import uuid
from django.urls import reverse_lazy

from feeds.models import Feed
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
        assert json_content['data'][0]['is_read'] == False
