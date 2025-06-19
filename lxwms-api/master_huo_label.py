import requests
from const import orders
import time
url = 'http://ops.masterhuo.com/edi/web-services/v2/createOneParcel'

import json
class Item:
    def __init__(self,  data: dict):
        self.name = 'pencil&markers'
        self.sku = data['SKU']
        self.length = data["Length"]
        self.width = data['Width']
        self.height = data['Height']
        self.weight = data['Weight']
        self.quantity = data['Outbound Qty']

class OrderDetail:
    def __init__(self, data: dict):
        # Map JSON keys to instance attributes with type conversion
        self.outbound_order_no = data.get("Outbound Order No", "")
        self.recipient = data.get("Recipient", "")
        self.telephone = data.get("Telephone", "")
        self.country = data.get("Country", "")
        self.province = data.get("Province", "")
        self.city = data.get("City", "")
        self.post_code = str(data.get("Post code", ""))  # Convert to string
        self.address1 = data.get("Address1", "")
        self.items = []
        self.addItem(data)
        # self.quantity = 
    
    def addItem(self, data):
        item = Item(data)
        self.items.append(item)

    @classmethod
    def from_dict(cls, data: dict) -> 'OrderDetail':
        """Factory method to create OrderDetail from dictionary"""
        return cls(data)


    def __repr__(self):
        return f"<OrderDetail: {self.outbound_order_no}, {self.city}, {self.post_code}>"


order_detail_map = {}
for o in orders:
    if o['Outbound Order No'] in order_detail_map:
        order_detail_map[o['Outbound Order No']].addItem(o)
    else:
        order = OrderDetail.from_dict(o)
        order_detail_map[o['Outbound Order No']] = order

i = 0
for o in orders:
    order  = order_detail_map[o['Outbound Order No']]
    expressCargos = []
    for item in order.items:
        expressCargos.append( {
                "cargoName": "",
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
                "usdValuePerUnit": 14.99,
                "usdValueTtl": 0,
                "vol": 0,
                "width": item.width
            })
    payload = {
        "bizType": "",
        "cargoValueUsd": "16.99",
        "channel": "美西268",
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
        "shipperAddressLineOne": "632 El Camino Real",
        "shipperAddressLineThree": "",
        "shipperAddressLineTwo": "",
        "shipperAttentionName": "",
        "shipperCity": "South San Francisco",
        "shipperCompanyName": "",
        "shipperCountryCode": "US",
        "shipperEmailAddress": "",
        "shipperPhoneNumber": "",
        "shipperPostalCode": "94080",
        "shipperProvinceCode": "CA",
        "shiptoAddressLineOne": order.address1,
        "shiptoAddressLineThree": "",
        "shiptoAddressLineTwo": "",
        "shiptoAttentionName": order.recipient,
        "shiptoCity": order.city,
        "shiptoCode": "",
        "shiptoCompanyName": "W2505104TK",
        "shiptoCountryCode": "US",
        "shiptoEmailAddress": "",
        "shiptoPhoneNumber": order.telephone,
        "shiptoPostalCode": order.post_code.zfill(5),
        "shiptoProvinceCode": order.province.split('(')[1][:-1].upper(),
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
    i+=1
    if i%20 == 0:
        time.sleep(2)
        i = 0
