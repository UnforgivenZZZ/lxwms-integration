import requests 
import json
import time
import hmac
import hashlib
import urllib.parse
import base64
import argparse
import os
import lxwms_utils as lxutil
from datetime import datetime, timedelta

COOKIE = 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22197394243b12109-0c391dfd54c57f-19525636-1484784-197394243b22bd2%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk3Mzk0MjQzYjEyMTA5LTBjMzkxZGZkNTRjNTdmLTE5NTI1NjM2LTE0ODQ3ODQtMTk3Mzk0MjQzYjIyYmQyIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%7D; _hjSessionUser_3119560=eyJpZCI6ImE0ZmJkZTZlLWM3OTMtNTU1YS1iZGNiLTBiYzhlOGI1ZmNlYyIsImNyZWF0ZWQiOjE3NDkwMTIzMzM2MDEsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.1600270249.1750016592; version=prod; language=cn; _ga_NRLS16EKKE=GS2.1.s1750059670$o32$g1$t1750059671$j59$l0$h0; _ga=GA1.1.1795520262.1749012333; _hjSession_3119560=eyJpZCI6IjlhNDUzZjk5LTU0MzgtNDkwNi04YjQ3LWYzODU3MTBiZWE1MSIsImMiOjE3NTAxMzA1OTQwNjAsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_2HTV43T3DN=GS2.1.s1750130594$o35$g0$t1750130594$j60$l0$h0; prod=always; sidebarStatus=0'
AUTHTOKEN = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIlN0IlMjJidXNpbmVzc1R5cGUlMjIlM0ElMjJ3bXMlMjIlMkMlMjJsb2dpbkFjY291bnQlMjIlM0ElMjJ6aG91amlhbGlhbmclMjIlMkMlMjJ1c2VyTmFtZUNuJTIyJTNBJTIyJUU1JTkxJUE4JUU1JTk4JTg5JUU0JUJBJUFFJTIyJTJDJTIydXNlck5hbWVFbiUyMiUzQSUyMiUyMiUyQyUyMmN1c3RvbWVyQ29kZSUyMiUzQW51bGwlMkMlMjJ0ZW5hbnRDb2RlJTIyJTNBJTIyMjUxNSUyMiUyQyUyMnRlcm1pbmFsVHlwZSUyMiUzQW51bGwlN0QiLCJpc3MiOiJ4aW5nbGlhbi5zZWN1cml0eSIsImJ1c2luZXNzVHlwZSI6IndtcyIsImV4cCI6MTc0OTMyMTA2NiwiaWF0IjoxNzQ5MjM0NjY2LCJqdGkiOiIwZThjMTBjMi02MGRhLTRkYTQtYTYyYi1hNmIyMjQ4MDFjOWEifQ.3Tz8vFsoqumDyywEHyaVlJ8dXJ1UkcgobiPfO_kosic'

class Item:
    def __init__(self,  data: dict, appKey, secret):
        self.name = data['productAliasName']
        self.sku = data['sku']
        self.quantity = data['quantity']
        self.get_item_detail(appKey, secret)

    def get_item_detail(self, appKey, secret):
        headers = {
            "Content-Type": "application/json"
        }
        data={'appKey': appKey}
        data['reqTime'] = str(int(time.time()))
        data['data'] = {}
        data['data']['skuList'] = [self.sku]
        business_data = data['data']
        req_time = data["reqTime"]
        authcode = lxutil.generate_lxwms_authcode(app_key, secret, business_data, req_time)
        host = f"https://api.xlwms.com/openapi/v1/product/pagelist?authcode={authcode}"
        response = requests.post(host, headers=headers, data=json.dumps(data)).json()['data']['records'][0]
        # print(response)
        self.length = response["length"]
        self.lengthBs = response["lengthBs"]
        self.width = response['width']
        self.widthBs = response['widthBs']
        self.height = response['height']
        self.heightBs = response['heightBs']
        self.weight = response['weight']
        self.weightBs = response['weightBs']
        self.price = response['declarePrice']

    def __repr__(self):
        return f"{self.sku}-{self.quantity}"


class OrderDetail:
    def __init__(self, data: dict, key, secret, wave):
        # Map JSON keys to instance attributes with type conversion
        self.whCode = data['whCode']
        self.wave = wave
        self.outbound_order_no = data['outboundOrderNo']
        self.recipient = data.get("receiver", "")
        self.telephone = data.get("telephone", "")
        self.country_code = data.get("countryRegionCode", "")
        self.province_code = data.get("provinceCode", "")
        self.city = data.get("cityName", "")
        self.post_code = str(data.get("postCode", ""))  # Convert to string
        self.address = f"{data.get('houseNum', '')} {data.get('addressOne', '')} {data.get('addressTwo', '')} "
        self.items = []
        self.addItem(data['productList'], key, secret)
    
    def addItem(self, data, key, secret):
        for i in data:
            item = Item(i, key, secret)
            self.items.append(item)

    @classmethod
    def from_dict(cls, data: dict) -> 'OrderDetail':
        """Factory method to create OrderDetail from dictionary"""
        return cls(data)


    def __repr__(self):
        return f"<OrderDetail: {self.outbound_order_no}, {self.city}, {self.post_code}>"
    
    def get_sorted_sku(self):
        return sorted([str(item) for item in self.items])
    

def parse_order(data, key, secret, wave):
    for _ in range(5):
        try:
            order = OrderDetail(data,  key, secret, wave)
            res = lxutil.generate_master_huo_label(order)
            res['skus'] = order.get_sorted_sku()
            RES.write(f"{data['outboundOrderNo']},{json.dumps(res)}\n")
            PO.write(res['description']+'\n')
            return 1
        except Exception as e:
            print(data['whCode'], '\t', data['outboundOrderNo'], e)
            # raise e
            ERR.write(f"{data['whCode']}'\t'{data['outboundOrderNo']}\n")
            time.sleep(10)
    return 0

def parse_easyship(data, key, secret, wave):
    for _ in range(5):
        try:
            order = OrderDetail(data,  key, secret, wave)
            res = lxutil.create_easyship(order)
            res['skus'] = order.get_sorted_sku()
            RES.write(f"{data['outboundOrderNo']},{json.dumps(res)}\n")
            return 1
        except Exception as e:
            print(data['whCode'], '\t', data['outboundOrderNo'], e)
            # raise e
            ERR.write(f"{data['whCode']}'\t'{data['outboundOrderNo']}\n")
            time.sleep(10)
    return 0


def get_outbound_order_detail(data, secret, app_key, outboundOder, wave):
    headers = {
        "Content-Type": "application/json"
    }
    data['reqTime'] = str(int(time.time()))
    data['data'] = {}
    data['data']['outboundOrderNoList'] = [outboundOder]
    business_data = data['data']
    req_time = data["reqTime"]
    authcode = lxutil.generate_lxwms_authcode(app_key, secret, business_data, req_time)
    host = f"https://api.xlwms.com/openapi/v1/outboundOrder/detail?authcode={authcode}"
    response = requests.post(host, headers=headers, data=json.dumps(data)).json()
    if not response['data'][0]['logisticsTrackNo'] and response['data'][0]['logisticsChannel'] == 'No_Shipping_Service':
        return parse_order(response['data'][0], app_key, secret, wave)
        # print(f"{outboundOder}\t{response['data'][0]['logisticsTrackNo']}\t{response['data'][0]['logisticsCarrier']}\n")
        # weired_order.write(f"{outboundOder}\t{response['data'][0]['logisticsTrackNo']}\t{response['data'][0]['logisticsCarrier']}\n")
    elif not response['data'][0]['logisticsTrackNo'] and response['data'][0]['logisticsChannel'] == 'usps':
        return parse_easyship(response['data'][0], app_key, secret, wave)
    else:
        print(f"{outboundOder} tracling: {response['data'][0]['logisticsTrackNo']}")
        return 0
    
def get_outbound_by_wave(wave, wh_code, app_key, secret):
    url = "https://omp.xlwms.com/gateway/wms/blWaveDtl/dtl/page?current={page}&size=200&waveNo={wave}&whCode={wh_code}&productSku="
    headers = {
        "content-type": "application/json",
        "cookie": COOKIE,
        "authorization": AUTHTOKEN
    }
    pg = 1
    labels = 0
    while True:
        response = requests.get(url.format(page=pg, wave=wave, wh_code=wh_code), headers=headers)
        if response.json()['data']['records']:
            for o in response.json()['data']['records']:
                labels+=get_outbound_order_detail({"appKey": app_key}, secret, app_key,o['sourceNo'], f"{wave}_{pg}")
                # break
                
        else:
            break
        # break
        pg+=1
    # print(response.json())
    print(labels)


def check_inbound_detail(data, secret, app_key, wave):
    
    headers = {
        "Content-Type": "application/json"
    }
    # Send the POST request
    
    pg = 1
    cnt = 0
    reqs=  0
    while True:
        data['reqTime'] = str(int(time.time()))
        data['data']['page'] = pg 
        business_data = data['data']
        req_time = data["reqTime"]
        authcode = lxutil.generate_lxwms_authcode(app_key, secret, business_data, req_time)
        host = f"https://api.xlwms.com/openapi/v1/outboundOrder/pageList?authcode={authcode}"
        response = requests.post(host, headers=headers, data=json.dumps(data))
        # print(response.json())
        ls = response.json()['data']['records']
        if not ls:
            break
        for l in ls:
        #    print(l)
           if l['status'] == 2 and l['logisticsChannel'] == 'No_Shipping_Service':
                
                cnt+=get_outbound_order_detail({"appKey": app_key}, secret, app_key,l['outboundOrderNo'], wave)
                break
           elif l['status'] == 2 and l['logisticsChannel'] == 'Upload_Shipping_Label':
               pass

        pg+=1
        # break
    print(cnt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check if there is new inbound order")
        # Define the command-line arguments
    parser.add_argument('--customerName', required=True, help="name of customer: ie: ")
    parser.add_argument('--wave', required=True, help="name of customer: ie: ")
    parser.add_argument('--whCode', required=True, help="name of customer: ie: ")
    args = parser.parse_args()
    app_secret = os.getenv(f"{args.customerName}_secret")
    app_key = os.getenv(f"{args.customerName}_key")

    data  = {
        "appKey": app_key,
        "reqTime": str(int(time.time())) ,
        "data": {
            "page": 1,
            "endTime": "2025-05-12 23:59:59",
            "pageSize": 50
        }
    }
    # check_inbound_detail(data, app_secret, app_key, args.wave)
    RES = open(f'{args.wave}.txt', 'w')
    ERR = open(f'{args.wave}_err.txt', 'w')
    PO = open(f'{args.wave}_po.txt', 'w')
    get_outbound_by_wave(args.wave, args.whCode, app_key, app_secret)
