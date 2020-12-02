import requests
from bs4 import BeautifulSoup
from pprint import pprint


from .cardfinder import CardFinder


class EVGA(CardFinder):

    def get_card_name(self, elem):
        div = elem.find('div', class_="pl-list-pname")
        return div.find('a').get_text().strip()

    def get_card_href(self, elem):
        div = elem.find('div', class_="pl-list-pname")
        return div.find('a').get('href')

    def has_card_stock(self, elem):
        para = elem.find('p', class_="message-information")
        if not para:
            return True
        return not "Out of Stock" in para.get_text()

    def build_card_info(self, results):
        card_elems = results.find_all('div', class_='list-item')
        card_info = []
        for card in card_elems:
            card_info.append({
                'store': 'EVGA Direct',
                'name': self.get_card_name(card),
                'href': self.get_card_href(card),
                'has_stock': self.has_card_stock(card),
                'stock_info': {},
            })
        return card_info

    def get_stock_info(self):
        page = self.make_request(
            'https://www.evga.com/products/productlist.aspx?type=0&family=GeForce+30+Series+Family&chipset=RTX+3080'
        )

        soup = BeautifulSoup(page.content, 'html.parser')
        return self.build_card_info(soup)


if __name__ == '__main__':
    pprint(MemoryExpress().get_stock_info())