import requests
from bs4 import BeautifulSoup
from pprint import pprint


from fake_useragent import UserAgent
ua = UserAgent()


class CardFinder:
    def __init__(self):
        self._ua = UserAgent()

    @property
    def _headers(self):
        return {'User-Agent': ua['Internet Explorer']}

    def make_request(self, url):
        return requests.get(url, headers=self._headers)

    def get_stock_info(self):
        return []