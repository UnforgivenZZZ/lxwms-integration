import requests 
import json
import time
import hmac
import hashlib
import urllib.parse
import base64
import argparse
import os
from datetime import datetime, timedelta

def download_and_save_file(data, path):
    # Extract relevant information from the data
    job_number = data['jobNum']
    tracking_number = data['trackingNum']
    file_url = data['labelUrl']
    
    # Create directory path using job number
    base_dir = os.path.join('downloads', path)
    os.makedirs(base_dir, exist_ok=True)
    
    # Create file path using tracking number
    file_path = os.path.join(base_dir, f'{tracking_number}.pdf')
    
        # Download the file

    
    # Save the file
    retries = 0
    while retries < 5:
        try:
            response = requests.get(file_url)
            response.raise_for_status()  # Check for HTTP errors
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
                # print( f"File successfully saved to: {os.path.abspath(file_path)}")
                return
        except Exception as e:
            retries+=1
            if retries == 5:
                raise e
            else:
                time.sleep(10)
                continue


def generate_lxwms_authcode(app_key_value, app_secret, data_dict, req_time_value):
    # 1. 从 data 中提取出 appKey 和 reqTime，删除它们
    
    # 2. 对 data 内部字段进行排序（不区分大小写）
    sorted_data = {k: data_dict[k] for k in sorted(data_dict, key=str.lower)}
    
    # 3. 将排序后的 data 转为 JSON 字符串
    data_json = json.dumps(sorted_data, separators=(',', ':'), ensure_ascii=False)

    # 4. 构造拼接字符串
    sign_string = app_key_value + data_json + req_time_value
    # print(sign_string)

    # 5. 使用 appSecret 对拼接字符串进行 HMAC-SHA256 加密
    authcode = hmac.new(
        key=app_secret.encode('utf-8'),
        msg=sign_string.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    return authcode

# def get_pre_upload_label_order(order)

def generate_master_huo_label(order):
    url = 'http://ops.masterhuo.com/edi/web-services/v2/createOneParcel'
    expressCargos = []
    for item in order.items:
        expressCargos.append( {
                "cargoName": item.name,
                "cargoNameEn": "",
                "code": "",
                "gw": item.weight,
                "height": item.height,
                "hsCode": "",
                "length": item.length,
                "originalCountry": "US",
                "packageType": "PACKAGES",
                "pkgs": item.quantity,
                "quantity": item.quantity,
                "remarks": "",
                "sku": item.sku,
                "usdValuePerUnit": item.price,
                "usdValueTtl": 0,
                "vol": 0,
                "width": item.width
            })
    payload = {
        "bizType": "",
        "cargoValueUsd": "16.99",
        "channel": "AID-美西268",
        "collect": 0,
        "collectCur": "",
        "etd": "",
        "expressCargos": expressCargos,
        "goodsDiscription": "Pencils",
        "gw": 0,
        "hsCode": "",
        "importerTaxId": "",
        "mblNum": "",
        "payParty": "CC",
        "pkgNum": 1,
        "pkgType": "PACKAGES",
        "poNum": f"{order.outbound_order_no}",
        "remarks": "",
        "shipmentType": "PARCEL",
        "shipperAddressLineOne": "245 S Spruce Ave #800",
        "shipperAddressLineThree": "",
        "shipperAddressLineTwo": "",
        "shipperAttentionName": "Ricky Tran",
        "shipperCity": "South San Francisco",
        "shipperCompanyName": "",
        "shipperCountryCode": "US",
        "shipperEmailAddress": "",
        "shipperPhoneNumber": "",
        "shipperPostalCode": "94080",
        "shipperProvinceCode": "CA",
        "shiptoAddressLineOne": order.address,
        "shiptoAddressLineThree": "",
        "shiptoAddressLineTwo": "",
        "shiptoAttentionName": order.recipient,
        "shiptoCity": order.city,
        "shiptoCode": "",
        "shiptoCompanyName": order.wave,
        "shiptoCountryCode": order.country_code,
        "shiptoEmailAddress": "",
        "shiptoPhoneNumber": order.telephone,
        "shiptoPostalCode": order.post_code.zfill(5),
        "shiptoProvinceCode": order.province_code,
        "soNum": "1",
        "vol": 0
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'appKey': '4cCErfB7Ijh6WAR63DYeJbfjJtc#g@dm',
        'appToken': 'gwKzzZL0p@rySCNF#R~@dG2dkrEM3LGh9QS_kqbpslf4m3L@xLmnl0yXvmNar^7lbFi7jY9Fg#eqqdJEVVL_qZLgGe4G0q8q48^WsF@QQTQBZW1W9AUJJo9d^llOEkGKh0_ARm3hVShkEC@V7Q05KNBx6jRX@Is4##b#B48CxU3xJfYKOUx^nRYLDutN#v#Eqmt$3bM#hz4tAKixRTxXj#g@0k5~4DWNvbCaSxs6w#cT__xC#p6Ir$t^^$da1R2'
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text+",")
    return response.json()


def generate_master_huo_label_print(order):
    url = 'http://ops.masterhuo.com/edi/web-services/v3/createParcelLabel'
    expressCargos = []
    for item in order.items:
        expressCargos.append( {
                "cargoName": item.name,
                "cargoNameEn": "",
                "code": "",
                "gw": item.weight,
                "height": item.height,
                "hsCode": "",
                "length": item.length,
                "originalCountry": "US",
                "packageType": "PACKAGES",
                "pkgs": item.quantity,
                "quantity": item.quantity,
                "remarks": "",
                "sku": item.sku,
                "usdValuePerUnit": item.price,
                "usdValueTtl": 0,
                "vol": 0,
                "width": item.width
            })
    payload = {
        "asynTask": False,
        "bizType": "",
        "cargoValueUsd": "16.99",
        "labelChannelName": "AID-美西268",
        "collect": 0,
        "collectCur": "",
        "etd": "",
        "expressCargos": expressCargos,
        "goodsDiscription": "Pencils",
        "gw": 0,
        "hsCode": "",
        "importerTaxId": "",
        "mblNum": "",
        "payParty": "CC",
        "pkgNum": 1,
        "pkgType": "PACKAGES",
        "poNum": f"{order.outbound_order_no}",
        "remarks": "",
        "shipmentType": "PARCEL",
        "shipperAttentionName": "Garcia Will",
        "shipperAddressLineOne": "9015 G St",
        "shipperAddressLineThree": "",
        "shipperAddressLineTwo": "",
        "shipperAttentionName": "",
        "shipperCity": "Oakland",
        "shipperCompanyName": "",
        "shipperCountryCode": "US",
        "shipperEmailAddress": "",
        "shipperPhoneNumber": "",
        "shipperPostalCode": "94621",
        "shipperProvinceCode": "CA",
        "shiptoAddressLineOne": order.address,
        "shiptoAddressLineThree": "",
        "shiptoAddressLineTwo": "",
        "shiptoAttentionName": order.recipient,
        "shiptoCity": order.city,
        "shiptoCode": "",
        "shiptoCompanyName": order.wave,
        "shiptoCountryCode": order.country_code,
        "shiptoEmailAddress": "",
        "shiptoPhoneNumber": order.telephone,
        "shiptoPostalCode": order.post_code.zfill(5),
        "shiptoProvinceCode": order.province_code,
        "soNum": "1",
        "vol": 0
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'appKey': '4cCErfB7Ijh6WAR63DYeJbfjJtc#g@dm',
        'appToken': 'gwKzzZL0p@rySCNF#R~@dG2dkrEM3LGh9QS_kqbpslf4m3L@xLmnl0yXvmNar^7lbFi7jY9Fg#eqqdJEVVL_qZLgGe4G0q8q48^WsF@QQTQBZW1W9AUJJo9d^llOEkGKh0_ARm3hVShkEC@V7Q05KNBx6jRX@Is4##b#B48CxU3xJfYKOUx^nRYLDutN#v#Eqmt$3bM#hz4tAKixRTxXj#g@0k5~4DWNvbCaSxs6w#cT__xC#p6Ir$t^^$da1R2'
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text+",")
    return response.text



def create_easyship(order):
    url = "https://public-api.easyship.com/2024-09/shipments"
    items = []
    for item in order.items:
        items.append({
            "description": item.name,
            "category": None,
            "hs_code": "123456",
            "contains_battery_pi966": False,
            "contains_battery_pi967": False,
            "contains_liquids": False,
            "sku": item.sku,
            "origin_country_alpha2": "US",
            "quantity": item.quantity,
            "dimensions": {
                "length": item.length,
                "width": item.width,
                "height": item.height
            },
            "actual_weight": item.weight,
            "declared_currency": "USD",
            "declared_customs_value": item.price
        })
    payload = {
        "origin_address": {
            "line_1": "307 Corey Way",
            "line_2": None,
            "postal_code": "94080",
            "country_alpha2": "US",
            "state": "California",
            "city": "South San Francisco",
            "contact_name": "E.Z",
            "company_name": "Shany Im&Ex Inc",
            "contact_phone": "626-623-9130",
            "contact_email": "unforgiven4396@gmail.com"
        },
            "origin_address_id": "4a1854b3-9088-4b64-b2b3-4799e3e713fa",
        "destination_address": {
            "line_1": order.address,
            "line_2": None,
            "postal_code": str(order.post_code).zfill(5),
            "state": order.province_code,
            "city": order.city,
            "country_alpha2": "US",
            "contact_name": order.recipient,
            "contact_phone": order.telephone,
            "contact_email": f"{order.outbound_order_no}@na.com"
        },
        # "incoterms": None,
        "order_data": {
            "platform_order_number": ' '.join(order.get_sorted_sku()),
            "platform_name": "Direct Sales"
        },
        "incoterms": 'DDP',
          "set_as_residential": True,

        "insurance": { "is_insured": False },
        "courier_settings": {
            "allow_fallback": False,
            "apply_shipping_rules": False,
            "courier_service_id": "c3e97b11-2842-44f1-84d1-afaa6b3f0a7c"

        },
        "shipping_settings": {
            "additional_services": { "qr_code": "none" },
            "units": {
                "weight": "kg",
                "dimensions": "cm"
            },
            "buy_label": True,
            "buy_label_synchronous": True,
            "printing_options": {
                "format": "pdf",
                "label": "4x6",
                "commercial_invoice": "4x6",
                "packing_slip": "4x6"
            }
        },
        "parcels": [
            {
                "box": None,
                "items": items,
                
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'Authorization': 'Bearer prod_v+dAaRrxWcpudhQcpZ2Vfz1G2KdaE2tP3k3iOe0Zkr0='
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)
    return response.json()

def get_job_by_track(track):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'appKey': '4cCErfB7Ijh6WAR63DYeJbfjJtc#g@dm',
        'appToken': 'gwKzzZL0p@rySCNF#R~@dG2dkrEM3LGh9QS_kqbpslf4m3L@xLmnl0yXvmNar^7lbFi7jY9Fg#eqqdJEVVL_qZLgGe4G0q8q48^WsF@QQTQBZW1W9AUJJo9d^llOEkGKh0_ARm3hVShkEC@V7Q05KNBx6jRX@Is4##b#B48CxU3xJfYKOUx^nRYLDutN#v#Eqmt$3bM#hz4tAKixRTxXj#g@0k5~4DWNvbCaSxs6w#cT__xC#p6Ir$t^^$da1R2'
    }
    url = f'http://ops.masterhuo.com/edi/web-services/v3/tracking?trackingRef={track}'
    req = requests.get(url=url, headers=headers)
    return req.json()['jobNum']

def get_label_by_job(job):
    url = 'http://ops.masterhuo.com/edi/web-services/getOneOrder?'
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        'appKey': '4cCErfB7Ijh6WAR63DYeJbfjJtc#g@dm',
        'appToken': 'gwKzzZL0p@rySCNF#R~@dG2dkrEM3LGh9QS_kqbpslf4m3L@xLmnl0yXvmNar^7lbFi7jY9Fg#eqqdJEVVL_qZLgGe4G0q8q48^WsF@QQTQBZW1W9AUJJo9d^llOEkGKh0_ARm3hVShkEC@V7Q05KNBx6jRX@Is4##b#B48CxU3xJfYKOUx^nRYLDutN#v#Eqmt$3bM#hz4tAKixRTxXj#g@0k5~4DWNvbCaSxs6w#cT__xC#p6Ir$t^^$da1R2'
    }
    req = requests.get(f"{url}jobNum={job}", headers=headers)
    res = req.json()
    return res

