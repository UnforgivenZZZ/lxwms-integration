import requests
import json, os, time
import pandas as pd
import argparse


url = 'http://ops.masterhuo.com/edi/web-services/getOneOrder?'
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    'appKey': '4cCErfB7Ijh6WAR63DYeJbfjJtc#g@dm',
    'appToken': 'gwKzzZL0p@rySCNF#R~@dG2dkrEM3LGh9QS_kqbpslf4m3L@xLmnl0yXvmNar^7lbFi7jY9Fg#eqqdJEVVL_qZLgGe4G0q8q48^WsF@QQTQBZW1W9AUJJo9d^llOEkGKh0_ARm3hVShkEC@V7Q05KNBx6jRX@Is4##b#B48CxU3xJfYKOUx^nRYLDutN#v#Eqmt$3bM#hz4tAKixRTxXj#g@0k5~4DWNvbCaSxs6w#cT__xC#p6Ir$t^^$da1R2'
}

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
    response = requests.get(file_url)
    response.raise_for_status()  # Check for HTTP errors
    
    # Save the file
    retries = 0
    while retries < 5:
        try:
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
    

# 准备存储数据的列表
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check if there is new inbound order")
        # Define the command-line arguments
    parser.add_argument('--wave', required=True, help="name of customer: ie: ")
    args = parser.parse_args()
    data = []
    with open(f'{args.wave}.txt', 'r') as f:
        for order in f.readlines():
            po = order.split(',')[0]
            order = json.loads(order[len(order.split(',')[0])+1:])
            
            try:
                # # 发送API请求
                # response = requests.get(
    
                # 提取需要的数据
                # download_and_save_file(order, args.wave)
                row = {
                    "Outbound Order Num/出库单号": po,
                    "Shipping service/承运商": "USPS",  # 固定值
                    "Tracking Number/物流跟踪号": order['trackingNum']
                }
                data.append(row)
                
                
                # 打印控制台日志（可选）
                print(f"Processed: {order['jobNum']}")
                
            except Exception as e:
                print(f"Error processing {po}: {e}")

    # 创建DataFrame
    df = pd.DataFrame(data)

    # 写入Excel文件
    try:
        df.to_excel(
            f"{args.wave}_tracking.xlsx",
            index=False,
            engine='openpyxl',
            columns=["Outbound Order Num/出库单号", "Shipping service/承运商", "Tracking Number/物流跟踪号"]
        )
        print(f"\nExcel文件已成功生成：{args.wave}_tracking.xlsx")
    except Exception as e:
        print(f"写入Excel文件时出错: {str(e)}")