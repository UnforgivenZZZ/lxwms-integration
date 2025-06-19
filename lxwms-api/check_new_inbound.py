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

def generate_authcode(app_key_value, app_secret, data_dict, req_time_value):
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

# 生成钉钉签名
def generate_dingtalk_sign(secret):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f"timestamp={timestamp}&sign={sign}"

# 发送钉钉消息
def send_dingtalk_message(content):
    # 设置请求头
    headers = {
        'Content-Type': 'application/json',
    }

    # 钉钉的Webhook URL (不包含timestamp和sign参数)
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=421c1d2bd24d83254af0b2fdda35afe4be579344e236c64f12174336cc990d0c'
    
    # 钉钉的密钥
    secret = 'SEC5cfd5c5adefac42fca644eb0040677ed2a203f1cfb1bd45b5d4e748233c13b30'

    
    # 生成签名
    sign = generate_dingtalk_sign(secret)
    
    # 拼接带有timestamp和sign的URL
    url_with_sign = f"{webhook_url}&{sign}"
    
    # 消息体
    data = {
        "msgtype": "text",  # 消息类型
        "text": {
            "content": f"This is a test\n\n{content}"  # 发送的文本内容
        }
    }
    
    # 发送POST请求
    response = requests.post(url_with_sign, headers=headers, data=json.dumps(data))

    # 打印响应结果
    print(response.json())

    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败", response.status_code, response.text)



def generate_msg(inbound_orders):
    if not inbound_orders:
        return
    msg = []
    print(inbound_orders)
    for inbound_order in inbound_orders:
        infos = [f"'仓库/whCode': {inbound_order['whCode']}"]
        infos.append(f"'单号/inboundOrderNo: {inbound_order['inboundOrderNo']}")
        infos.append(f"'预计抵达/expectedDate: {inbound_order['expectedDate']}")
        msg.append(' '.join(infos))
    return '\n\n'.join(msg)


def get_end_time(startTime, duration_minutes=5) -> str:
    # Convert string to datetime object
    st = datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")

    # Add 5 minutes
    new_time = st + timedelta(minutes=duration_minutes)
    
    # Convert new time back to string if needed
    return new_time.strftime("%Y-%m-%d %H:%M:%S")


def check_inbound_ourder(data, auth_key):
    host = f"https://api.xlwms.com/openapi/v1/inboundOrder/pageList?authcode={auth_key}"
    headers = {
        "Content-Type": "application/json"
    }
    # Send the POST request
    response = requests.post(host, headers=headers, data=json.dumps(data))
    msg = generate_msg(response.json()['data']['records'])
    print(response.json())
    print(msg)
    send_dingtalk_message(msg)


def check_out(data, auth_key):
    host = f"https://api.xlwms.com//openapi/v1/outboundOrder/detail?authcode={auth_key}"
    headers = {
        "Content-Type": "application/json"
    }
    # Send the POST request
    response = requests.post(host, headers=headers, data=json.dumps(data))
    print(response.json())


def check_inbound_detail(data, secret, app_key):
    
    headers = {
        "Content-Type": "application/json"
    }
    # Send the POST request
    
    with open('box.txt', 'w') as f:
        for order in ('IB003250402RV', 'IB003250402RU'):
            pg = 1
            while True:
                data['reqTime'] = str(int(time.time()))
                data['data']['page'] = pg 
                data['data']['inboundOrderNo'] = order
                business_data = data['data']
                req_time = data["reqTime"]
                authcode = generate_authcode(app_key, secret, business_data, req_time)
                host = f"https://api.xlwms.com/openapi/v1/inboundOrder/pageBoxSkuList?authcode={authcode}"
                response = requests.post(host, headers=headers, data=json.dumps(data))
                # print(response.json())
                ls = response.json()['data']['records']
                if not ls:
                    break
                for l in ls:
                    print(l['shippingMark'])
                    f.write(l['shippingMark']+'\n')
                pg+=1

def main(secret, key, startTime, endTime):
    data  = {
        "appKey": key,
        "reqTime": str(int(time.time())) ,
       "data": {
        "inboundOrderNo": "IB003250402RV",
        "inboundType": 1,
        "page": 1,
        "pageSize": 50
    }
    }
    # 提取 appKey 和 reqTime
    app_key = data["appKey"]
    req_time = data["reqTime"]

    # 获取业务数据并删除 appKey 和 reqTime
    # business_data = data['data']
    # authcode = generate_authcode(app_key, secret, business_data, req_time)
    check_inbound_detail(data, secret, app_key)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check if there is new inbound order")
        # Define the command-line arguments
    parser.add_argument('--customerName', required=True, help="name of customer: ie: JiZuo")
    parser.add_argument('--startTime', required=True, help="inbound order create time in yyyy-mm-dd hh:mm:ss format, Beijing Time")
    parser.add_argument('--endTime', required=True, help="inbound order create time in yyyy-mm-dd hh:mm:ss format, Beijing Time")
    # Parse the command-line arguments
    args = parser.parse_args()

    app_secret = os.getenv(f"{args.customerName}_secret")
    app_key = os.getenv(f"{args.customerName}_key")

    print(app_secret, app_key, args.startTime)
    main(app_secret, app_key, args.startTime, args.endTime)



