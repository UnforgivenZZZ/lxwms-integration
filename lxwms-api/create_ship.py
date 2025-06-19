import requests 

url = "https://public-api.easyship.com/2024-09/shipments"
orders = [
  {
    "Outbound Order No":"OBS0032505070SS",
    "Recipient":"Henry Phillips",
    "Telephone":"(+1)2707029628",
    "Country":"United States of America (USA)",
    "Province":"Kentucky(KY)",
    "City":"Philpot",
    "Post code":42366,
    "Address1":"6151 Highway 54",
    "Total Qty of SKU":1
  },
  {
    "Outbound Order No":"OBS0032505070SR",
    "Recipient":"Ysabella Tulod",
    "Telephone":"(+1)9095016917",
    "Country":"United States of America (USA)",
    "Province":"California(CA)",
    "City":"Loma Linda",
    "Post code":92354,
    "Address1":"26221 CITRON ST",
    "Total Qty of SKU":1
  },
  {
    "Outbound Order No":"OBS0032505070SQ",
    "Recipient":"Arif Alloo",
    "Telephone":"(+1)4843641230",
    "Country":"United States of America (USA)",
    "Province":"Pennsylvania(PA)",
    "City":"Sinking Spring",
    "Post code":19608,
    "Address1":"4712 Penn Ave PMB 305",
    "Total Qty of SKU":1
  }
]

# for order in orders:

def create_easyship(order):
    url = "https://public-api.easyship.com/2024-09/shipments"
    item = []
    for item in order.items:
        item.append({
            "description": "[组合]FC自动铅笔套装012-半金属6支装5792-FC标皮握银环(优绘大橡皮座)",
            "category": None,
            "hs_code": "123456",
            "contains_battery_pi966": False,
            "contains_battery_pi967": False,
            "contains_liquids": False,
            "sku": "X003OTYPGP",
            "origin_country_alpha2": "US",
            "quantity": 1,
            "dimensions": {
                "length": 21.5,
                "width": 15.5,
                "height": 1.8
            },
            "actual_weight": 0.39,
            "declared_currency": "USD",
            "declared_customs_value": 16.99
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
            "line_1": order['Address1'],
            "line_2": None,
            "postal_code": str(order['Post code']).zfill(5),
            "state": order['Province'].split('(')[0],
            "city": order['City'],
            "country_alpha2": "US",
            "contact_name": order['Recipient'],
            "contact_phone": order['Telephone'],
            "contact_email": "na@na.com"
        },
        # "incoterms": None,
        "order_data": {
            "platform_order_number": order['Outbound Order No'],
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
                "total_actual_weight": 0.39,
                "box": None,
                "items": [
                    {
                        "description": "[组合]FC自动铅笔套装012-半金属6支装5792-FC标皮握银环(优绘大橡皮座)",
                        "category": None,
                        "hs_code": "123456",
                        "contains_battery_pi966": False,
                        "contains_battery_pi967": False,
                        "contains_liquids": False,
                        "sku": "X003OTYPGP",
                        "origin_country_alpha2": "US",
                        "quantity": 1,
                        "dimensions": {
                            "length": 21.5,
                            "width": 15.5,
                            "height": 1.8
                        },
                        "actual_weight": 0.39,
                        "declared_currency": "USD",
                        "declared_customs_value": 16.99
                    }
                ]
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