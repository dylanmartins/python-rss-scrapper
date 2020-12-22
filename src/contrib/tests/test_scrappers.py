from unittest.mock import Mock

import pytest

from contrib.scrappers import RssScrapper


@pytest.mark.django_db
class TestRssScrapper:

    @pytest.fixture
    def valid_rss(self):
        return '''
            <rss xmlns:content="http://purl.org/rss/1.0/modules/content/" version="2.0">
            <channel>
            <pubDate>Mon, 21 Dec 2020 22:37:00 GMT</pubDate>
            <lastBuildDate>Mon, 21 Dec 2020 22:37:00 GMT</lastBuildDate>
            <item>
            <title>\'Among Us is met 500 miljoen actieve spelers meest populaire game ooit\'</title>
            <link>https://tweakers.net/nieuws/176016/among-us-is-met-500-miljoen-actieve-spelers-meest-populaire-game-ooit.html</link>
            <category>
            Nieuws - : Gaming / Games
            </category>
            <pubDate>Mon, 21 Dec 2020 20:38:00 GMT</pubDate>
            </item>
            </channel></rss>
        '''  # noqa

    @pytest.fixture
    def mock_valid_xml_content(self, valid_rss):
        mock = Mock()
        mock.status_code = 200
        mock.content = valid_rss
        return mock

    @pytest.fixture
    def mock_invalid_request(self):
        mock = Mock()
        mock.status_code = 500
        mock.content = ''
        return mock

    @pytest.fixture
    def scrapper(self):
        return RssScrapper()

    @pytest.fixture
    def url(self):
        return 'https://feeds.feedburner.com/tweakers/mixed'

    def test_scrappy_should_return_items_from_rss(
        self,
        url,
        scrapper,
        patch_requests_get,
        mock_valid_xml_content,
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_valid_xml_content
            results = scrapper.scrappy(url)

        assert results[0] == {
            'link': 'https://tweakers.net/nieuws/176016/among-us-is-met-500-miljoen-actieve-spelers-meest-populaire-game-ooit.html',  # noqa
            'published': 'Mon, 21 Dec 2020 20:38:00 GMT',
            'title': "'Among Us is met 500 miljoen actieve spelers meest populaire game ooit'"  # noqa
        }

    def test_scrappy_should_return_empty_list_if_status_diff_of_200(
        self,
        url,
        scrapper,
        patch_requests_get,
        mock_invalid_request,
    ):
        with patch_requests_get as mock_get:
            mock_get.return_value = mock_invalid_request
            results = scrapper.scrappy(url)

        assert results == []
