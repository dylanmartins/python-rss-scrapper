import logging

import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse

logger = logging.getLogger(__name__)


class RssScrapper:

    def _get_item_data(self, item):
        return {
            'title': item.find('title').text,
            'description': item.find('description').text,
            'published': item.find('pubDate').text,
            'link': item.find('link').text,
        }

    def scrappy(self, url):
        try:
            result = requests.get(url)
            if result.status_code != 200:
                return []

            soup = BeautifulSoup(result.content, features='xml')
            raw_items = soup.findAll('item')

            return [
                self._get_item_data(item)
                for item in raw_items
            ]
        except Exception as err:
            logger.error(f'Error scrapping data from url {url}. Error:{err}')
            raise
