import requests
import pandas as pd

HOST = 'https://api.tanwaos.com/recharge/getListNew'
HEADERS = {
    'authorization': 'Bearer PVNQFXWB9CGGVVMGTCPHXKDLA5ZNBNCZDOYVFCVRYJIK2JCF3Q',
    'sec-ch-ua-platform': 'macOS',
    'content-type': 'application/json;charset=UTF-8',
    'sec-fetch-site': 'same-site',
    'content-length': '96'


}
record = []
page = 1
while True:
    payload = {"lb":"1","page":page,"limit":100,"startTime":"2025-07-01 00:00:00","endTime":"2025-07-15 23:59:59"}
    print(payload)
    req = requests.post(HOST, headers=HEADERS, data=payload)
    print(req.json())
    cur_page = req.json()['data']['current_page']
    for ret in req.json()['data']['data']:
        print(ret['money'], ret['uptime'], ret['realmoney'], ret['nmoney'])
        record.append({
            'RMB': ret['money'], "USD": ret['realmoney'], "时间": ret['uptime']
        })
    if cur_page == req.json()['data']['last_page']:
        break
    page+=1
# Write to Excel
df = pd.DataFrame(record)
df.to_excel("recharge_records.xlsx", index=False)

print("Excel file saved: recharge_records.xlsx")