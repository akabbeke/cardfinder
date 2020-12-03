import requests
from bs4 import BeautifulSoup
from pprint import pprint

from .cardfinder import CardFinder

from requests_html import HTMLSession


class Nvidia(CardFinder):
    def get_card_name(self, elem):
        div = elem.find('h2', class_="name")
        return div.get_text().strip()

    def has_card_stock(self, elem):
        link = elem.find('a', class_="featured-buy-link")
        return "Out Of Stock" not in link.get_text()

    def build_card_info(self, results):
        card_elems = results.find_all('div', class_='product-details-container')
        card_info = []
        for card in card_elems:
            card_info.append({
                'store': 'Nvidia',
                'name': self.get_card_name(card),
                'href': 'N/A',
                'has_stock': self.has_card_stock(card),
                'stock_info': {},
            })
        return card_info

    def make_request(self, url):
        session = HTMLSession()
        r = session.get(url, headers=self._headers)
        r.html.render()
        return r.html.raw_html

    def get_stock_info(self,):
        page = self.make_request(
            "https://www.nvidia.com/en-ca/shop/geforce/?page=1&limit=9&locale=en-ca&gpu=RTX%203080,RTX%203090&manufacturer=NVIDIA&gpu_filter=RTX%203090~0,RTX%203080~1,RTX%203070~0,RTX%203060%20Ti~0,RTX%202080%20SUPER~0,RTX%202080~0,RTX%202070%20SUPER~0,RTX%202070~0,RTX%202060~0,GTX%201660%20Ti~0,GTX%201660%20SUPER~0,GTX%201660~0,GTX%201650%20Ti~0,GTX%201650%20SUPER~0,GTX%201650~0"
        )

        soup = BeautifulSoup(page, 'html.parser')

        results = soup

        return self.build_card_info(results)


if __name__ == '__main__':
    pprint(Nvidia().get_stock_info())