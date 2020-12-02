from cardfinder.memory_express import MemoryExpress
from cardfinder.canada_computers import CanadaComputers
from cardfinder.evga import EVGA

from pprint import pprint

def main():
    cc_data = MemoryExpress().get_stock_info()
    mm_data = CanadaComputers().get_stock_info()
    ev_data = EVGA().get_stock_info()

    all_data = cc_data + mm_data + ev_data

    for data in all_data:
        if data['has_stock']:
            pprint(data)

if __name__ == '__main__':
    main()