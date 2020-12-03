from cardfinder.memory_express import MemoryExpress
from cardfinder.canada_computers import CanadaComputers
from cardfinder.evga import EVGA
from cardfinder.nvidia import Nvidia
from cardfinder.newegg import NewEgg

from cardfinder.sms_client import SMSClient

from cardfinder.config import TARGET_NUMBERS

from pprint import pprint


from datetime import datetime



def format_alert(data):
    return '\n'.join([
        f"  STORE: {data['store']}",
        f"  MODEL: {data['name']}",
        f"  STOCK: {data['stock_info']}",
        '',
    ])

def main():
    cc_data = MemoryExpress().get_stock_info()
    mm_data = CanadaComputers().get_stock_info()
    ev_data = EVGA().get_stock_info()
    nv_data = Nvidia().get_stock_info()
    ne_data = NewEgg().get_stock_info()

    all_data = cc_data + mm_data + ev_data + nv_data + ne_data
    output = ['ALERT: STOCK FOUND!!']
    stock_found = False
    for data in all_data:
        if data['has_stock']:
            stock_found = True
            output.append(format_alert(data))

    if stock_found:
        for target in TARGET_NUMBERS:
            print('\n'.join(output))
            SMSClient().send_sms(target, '\n'.join(output))

    print("Ran at", datetime.now(), "Found:", stock_found, "Checked:", len(all_data))


if __name__ == '__main__':
    main()