import requests
from bs4 import BeautifulSoup
from pprint import pprint

from .cardfinder import CardFinder


class MemoryExpress(CardFinder):
    def get_card_name(self, elem):
        div = elem.find('div', class_="c-shca-icon-item__body-name")
        return div.find('a').get_text().strip()

    def has_card_stock(self, elem):
        div = elem.find('div', class_="c-shca-icon-item__body-extras")
        return not div.find('div', class_="c-shca-icon-item__body-inventory")

    def build_card_info(self, results):
        card_elems = results.find_all('div', class_='c-shca-icon-item')
        card_info = []
        for card in card_elems:
            card_info.append({
                'store': 'Memory Express',
                'name': self.get_card_name(card),
                'href': 'N/A',
                'has_stock': self.has_card_stock(card),
                'stock_info': {},
            })
        return card_info

    def get_stock_info(self,):
        page = self.make_request(
            'https://www.memoryexpress.com/Category/VideoCards?FilterID=45788ec3-6bb1-e460-abe6-afa274b9d30e&PageSize=80'
        )

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find('div', class_='c-cact-product-list__body')

        return self.build_card_info(results)


if __name__ == '__main__':
    pprint(MemoryExpress().get_stock_info())