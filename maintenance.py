from datetime import datetime
from openpyxl import *


# Get device information from excel file.
def get_device_info():
    file_name = 'swpm.xlsx'         # name of excel file
    device_list = 'device_lists'    # name of worksheet
    devices = list()
    book = load_workbook(file_name)
    sheet = book[device_list]
    for row in sheet.rows:
        tmp = dict()
        tmp['ip'] = row[0].value
        tmp['user'] = row[1].value
        tmp['password'] = row[2].value
        tmp['protocol'] = row[3].value
        tmp['port'] = row[4].value
        tmp['vendor'] = row[5].value
        tmp['check'] = row[6].value
        devices.append(tmp)
        del tmp
    header = {
        'ip': 'ip', 'user': 'user', 'password': 'password', 'protocol': 'protocol',
        'port': 'port', 'vendor': 'vendors', 'check': 'check',
    }
    if header in devices:
        devices.remove(header)
        return devices
    else:
        print('Please check excel file...')
        exit(0)


if __name__ == '__main__':
    print(get_device_info())
