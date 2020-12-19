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
        qty_feeds = Feed.objects.all().count()
        url = reverse_lazy('feeds:index')
        response = api_client.get(url)

        assert response.status_code == 200
        assert response.json() == {
            'data': [
                {'title': 'Test feed', 'url': 'http://www.nu.nl/rss/Algemeen'}
            ]
        }
        assert qty_feeds == 2
