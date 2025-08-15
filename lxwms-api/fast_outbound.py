import requests 
import pandas as pd
import json
import argparse

headers = {
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIlN0IlMjJidXNpbmVzc1R5cGUlMjIlM0ElMjJ3bXMlMjIlMkMlMjJsb2dpbkFjY291bnQlMjIlM0ElMjJ6aG91amlhbGlhbmclMjIlMkMlMjJ1c2VyTmFtZUNuJTIyJTNBJTIyJUU1JTkxJUE4JUU1JTk4JTg5JUU0JUJBJUFFJTIyJTJDJTIydXNlck5hbWVFbiUyMiUzQSUyMiUyMiUyQyUyMmN1c3RvbWVyQ29kZSUyMiUzQW51bGwlMkMlMjJ0ZW5hbnRDb2RlJTIyJTNBJTIyMjUxNSUyMiUyQyUyMnRlcm1pbmFsVHlwZSUyMiUzQW51bGwlN0QiLCJpc3MiOiJ4aW5nbGlhbi5zZWN1cml0eSIsImJ1c2luZXNzVHlwZSI6IndtcyIsImV4cCI6MTc1MDc4MzkwMiwiaWF0IjoxNzUwNjk3NTAyLCJqdGkiOiIyNDY2MjgwMS1jNDIyLTRhNGEtYWQwMi03YWFmZmI2ZThiZGIifQ.FbDXtfAZgNBSt1TNelZTGKmNlynVsLZjrjR07hJKpfQ',
    'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22197678eccb4f4d-0e1019d88768db8-1a525636-1484784-197678eccb527e7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3Njc4ZWNjYjRmNGQtMGUxMDE5ZDg4NzY4ZGI4LTFhNTI1NjM2LTE0ODQ3ODQtMTk3Njc4ZWNjYjUyN2U3In0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; version=prod; sidebarStatus=1; _hjSessionUser_3119560=eyJpZCI6IjNkOGZkNDFhLTUyNjItNWExOS05NjBiLWI0NzZkMjhmMDhiNCIsImNyZWF0ZWQiOjE3NDk3ODkxMDE0MDIsImV4aXN0aW5nIjp0cnVlfQ==; language=en; _gid=GA1.2.1477649513.1754021900; _hjSession_3119560=eyJpZCI6Ijc4MWU1YzcxLTIwNjQtNDJjMy05NjA3LTdiNjBmZGU0YTBiMCIsImMiOjE3NTQwOTQ4OTI0MjQsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_NRLS16EKKE=GS2.1.s1754094891$o132$g1$t1754094892$j59$l0$h0; _ga=GA1.1.987879918.1749789100; _ga_2HTV43T3DN=GS2.1.s1754094891$o185$g1$t1754096435$j60$l0$h0; prod=always',
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',

}
path = '/gateway/wms/blWave/quickDelivery'
host = 'https://omp.xlwms.com'


def isWavePicked(wave):
    url = f"https://omp.xlwms.com/gateway/wms/blWave/waveStatusSum?current=1&size=200&logisticsCarrier=&logisticsChannel=&orderType=&pickingType=&barcode=&orderNo={wave}&sortingFlag=&reviewFlag=&outboundFlag=&isAssignPicker=0&waveNoList%5B0%5D={wave}&whCode=LAX"
    req = requests.get(
        url,
        headers=headers,

    )
    resp = req.json()['data']
    for d in resp:
        if d['statusName'] == '已拣货' and d['statusSum'] == 1:
            return True
    return False

def getPickList(wave):
    url = f"https://omp.xlwms.com/gateway/wms/blWave/pickSkuList?waveNo={wave}&whCode=LAX"
    req = requests.get(
        url,
        headers=headers,

    )
    resp = req.json()
    return resp



def pick(wave):
    if isWavePicked(wave):
        print(f"{wave} picked")
        return
    resp = getPickList(wave)
    sku_list = []
    # print(resp)
    for ele in resp['data']['skuList']:
        for item in ele['reCommendCellList']:
            sku_list.append({
                "productSku": item['item'],
                "cellNo": item['cellNo'],
                "pickQty": int(item['qty']),
                "pickQty1": int(item['qty']),
                "productQuality": 0,
                "planQty": int(item['qty']),
                "customerCode": str(item['customerCode']),
                "id": f"{item['item']}{item['customerCode']}"
            })
    url = "https://omp.xlwms.com/gateway/wms/blWave/pcPick"
    print(resp)
    print({
            "deliveryNo": "",
            "waveNo": wave,
            "whCode": "LAX",
            "skuList": sku_list
             
            })
    req = requests.post(
        url, headers=headers, json={
            "deliveryNo": "",
            "waveNo": wave,
            "whCode": "LAX",
            "skuList": sku_list
             
            }
    )
    print(req.json())

def get_wave_order_number(wave):
    if not isWavePicked(wave):
        print(f"picking wave {wave}")
        pick(wave)
        
    query = f"waveNo={wave}&whCode=LAX"
    url = f"https://omp.xlwms.com/gateway/wms/blWave/detail?{query}"
    req = requests.get(
            url,
            headers=headers,

        )
    return req.json()['data']['totalCount']

def scan_to_outbound(filename: str):
    res = []
    while True:
        name = input("picker name: ")
        if name == 'finish':
            break
        while True:
            wave = input("scan wave: ")
            if wave == 'exit':
                break
            cnt = get_wave_order_number(wave)
            req = requests.post(
                f"{host}/{path}",
                headers=headers,
                json={'waveNo': wave, 'whCode': "LAX"}

            )
            print(req.json())
            # if req.json()['code'] != 400:
            res.append({'name/人员': name, "wave/波次": wave, "count/订单数量": cnt})

    df = pd.DataFrame(res)

    # Write to Excel
    df.to_excel(f"{filename}.xlsx", index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="todays date in yyyy-mm-dd format")
    parser.add_argument("--date", type=str, help="todays date in yyyy-mm-dd format")
    args = parser.parse_args()
    scan_to_outbound(args.date)