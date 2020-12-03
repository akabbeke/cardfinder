import requests
from bs4 import BeautifulSoup
from pprint import pprint

from .cardfinder import CardFinder

from requests_html import HTMLSession


class NewEgg(CardFinder):
    def get_card_name(self, elem):
        div = elem.find('a', class_="item-title")
        return div.get_text().strip()

    def get_card_href(self, elem):
        div = elem.find('a', class_="item-title")
        return div.get("href")

    def has_card_stock(self, elem):
        link = elem.find('p', class_="item-promo")
        return link is None

    def build_card_info(self, results):
        card_elems = results.find_all('div', class_='item-container')
        card_info = []
        for card in card_elems:
            print(card.prettify())
            card_info.append({
                'store': 'Nvidia',
                'name': self.get_card_name(card),
                'href': self.get_card_href(card),
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
            "https://www.newegg.ca/p/pl?N=100007708%20601357247"
        )

        soup = BeautifulSoup(page, 'html.parser')

        results = soup

        return self.build_card_info(results)


if __name__ == '__main__':
    pprint(NewEgg().get_stock_info())