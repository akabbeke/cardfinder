import requests
from bs4 import BeautifulSoup
from pprint import pprint

from .cardfinder import CardFinder


class CanadaComputers(CardFinder):

    def get_store_name(self, elem):
        div = elem.find('div', class_="col-9")
        if not div:
            return
        p = div.find('p')
        if not p:
            return
        if p.get_text():
            return p.get_text()
        link = p.find('a')
        if not link:
            return
        else:
            return link.get_text()

    def get_stock_number(self, elem):
        span = elem.find('span', class_="stocknumber")
        if not span:
            return
        if span.get_text():
            return span.get_text()
        strong = span.find('strong')
        if not strong:
            return
        else:
            return strong.get_text()


    def get_stock_id(self, elem):
        classes = elem.get('class')
        if len(classes) == 2 and 'stocklevel-pop-' in classes[1]:
            return classes[1].replace('stocklevel-pop-', '')


    def map_stock_number(self, value):
        if value == '-' or value is None:
            return 0
        elif value == '5+':
            return 5
        else:
            return int(value)

    def get_card_name(self, elem):
        return elem.find('a', class_="text-dark text-truncate_3").get_text()

    def get_card_href(self, elem):
        return elem.find('a', class_="text-dark text-truncate_3").get('href')

    def get_card_stock_id(self, elem):
        return elem.find('div', class_='productTemplate').get('data-item-id')

    def build_card_info(self, results):
        card_elems = results.find_all('div', class_='col-xl-3 col-lg-4 col-6 mt-0_5 px-0_5 toggleBox mb-1')
        card_info = []
        for card in card_elems:
            card_info.append({
                'name': self.get_card_name(card),
                'href': self.get_card_href(card),
                'stock_id': self.get_card_stock_id(card),
            })
        return card_info


    def build_stock_dict(self, results):
        stock_elems = results.find_all('div', class_='stocklevel-pop')

        stock_dict = {}
        for stock in stock_elems:
            stock_regions = stock.find_all('div', class_="row col-border-bottom pt-1")
            store_dict = {}
            for region in stock_regions:
                stores = region.find_all('div', class_="row")
                for store in stores:
                    if self.get_store_name(store):
                        store_dict[self.get_store_name(store)] = self.map_stock_number(self.get_stock_number(store))

            stock_dict[self.get_stock_id(stock)] = store_dict

        return stock_dict


    def available_stock(self, stock):
        return {x: stock[x] for x in stock if stock[x]}


    def get_stock_info(self):
        page = self.make_request(
            'https://www.canadacomputers.com/index.php?cPath=43&sf=:3_5&mfr=&pr='
        )

        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='product-list')

        stock_dict = self.build_stock_dict(results)
        card_info = self.build_card_info(results)
        shop_info = []
        for card in card_info:
            card_stock = stock_dict.get(card['stock_id'])

            if not card_stock:
                stock_info = {}
                has_stock = False
            else:
                stock_info = self.available_stock(card_stock)
                has_stock = bool(stock_info)

            shop_info.append({
                'store': 'Canada Computers',
                'name': card['name'],
                'href': card['href'],
                'has_stock': has_stock,
                'stock_info': stock_info,
            })

        return shop_info

if __name__ == '__main__':
    pprint(MemoryExpress().get_stock_info())