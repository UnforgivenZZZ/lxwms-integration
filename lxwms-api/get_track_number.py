import requests
import json, os, time
import pandas as pd
from PyPDF2 import PdfMerger
from io import BytesIO

wave = input('wave: ')
url = 'http://ops.masterhuo.com/edi/web-services/getOneOrder?'
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    'appKey': '4cCErfB7Ijh6WAR63DYeJbfjJtc#g@dm',
    'appToken': 'gwKzzZL0p@rySCNF#R~@dG2dkrEM3LGh9QS_kqbpslf4m3L@xLmnl0yXvmNar^7lbFi7jY9Fg#eqqdJEVVL_qZLgGe4G0q8q48^WsF@QQTQBZW1W9AUJJo9d^llOEkGKh0_ARm3hVShkEC@V7Q05KNBx6jRX@Is4##b#B48CxU3xJfYKOUx^nRYLDutN#v#Eqmt$3bM#hz4tAKixRTxXj#g@0k5~4DWNvbCaSxs6w#cT__xC#p6Ir$t^^$da1R2'
}

# 确保下载目录存在
base_dir = f'./downloads/{wave}'
os.makedirs(base_dir, exist_ok=True)

# 创建PDF合并器对象
pdf_merger = PdfMerger()

def download_pdf_to_memory(url):
    """下载PDF到内存并直接添加到合并器"""
    retries = 0
    while retries < 5:
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # 使用BytesIO将内容保存在内存中
            pdf_content = BytesIO(response.content)
            
            # 直接添加到合并器
            pdf_merger.append(pdf_content)
            return True
        except Exception as e:
            print(f"下载失败: {str(e)} - 重试 {retries+1}/5")
            retries += 1
            time.sleep(10)
    return False

# 读取PO列表并保留原始顺序
with open(f'{wave}.txt', 'r') as f:
    po_list = []
    for line in f:
        arr = line.split(',')
        po = arr[0].strip()
        print(json.loads(line[len(po)+1:])['skus'])
        skus = json.loads(line[len(po)+1:])['skus']
        po_list.append((len(skus), ";".join(skus), po))

def get_job_by_track(track):
    url = f'http://ops.masterhuo.com/edi/web-services/v3/tracking?trackingRef={track}'
    req = requests.get(url=url, headers=headers)
    print(req.json())

with open(f'{wave}_dwn.txt', 'w') as dwn:
    data = []
    success_count = 0
    failed_pos = []
    po_list.sort()
    # 按原始顺序处理每个PO
    for i, (_, skus, po) in enumerate(po_list, 1):
        print(f"\n处理PO ({i}/{len(po_list)}): {po}, {skus}")
        retries = 0
        success = False
        
        while retries < 5 and not success:
            try:
                # 获取PDF URLx
                req = requests.get(f"{url}poNum={po}", headers=headers)
                res = req.json()
                pdf_url = res['labelUrl']
                print(i)
                # 记录下载信息
                dwn.write(pdf_url + '\n')
                
                # 下载并直接添加到合并器（保持顺序）
                if download_pdf_to_memory(pdf_url):
                    print(f"✅ 成功下载: {po}")
                    
                    # 添加跟踪信息
                    data.append({
                        "Outbound Order Num/出库单号": po,
                        "Shipping service/承运商": "USPS",
                        "Tracking Number/物流跟踪号": res['trackingNum']
                    })
                    success = True
                    success_count += 1
                else:
                    print(f"⚠️ 失败: 无法下载 {po} 的PDF")
                    failed_pos.append(po)
                    break
                    
            except Exception as e:
                print(f"错误 ({po}): {str(e)} - 重试 {retries+1}/5")
                retries += 1
                time.sleep(10)
        
        if not success and retries >= 5:
            print(f"🚫 最终失败: 无法处理 {po}")
            failed_pos.append(po)

# 保存合并后的PDF
merged_pdf = os.path.join(base_dir, f'{wave}_combined.pdf')
with open(merged_pdf, 'wb') as output_pdf:
    pdf_merger.write(output_pdf)

print(f"\n✅ 所有PDF已合并到: {os.path.abspath(merged_pdf)}")
print(f"  成功合并: {success_count} 个PDF")
print(f"  失败PO: {len(failed_pos)} 个: {', '.join(failed_pos)}")

# 保存Excel跟踪信息
if data:
    df = pd.DataFrame(data)
    excel_file = f"{wave}_order_tracking.xlsx"
    df.to_excel(
        excel_file,
        index=False,
        engine='openpyxl',
        columns=["Outbound Order Num/出库单号", "Shipping service/承运商", "Tracking Number/物流跟踪号"]
    )
    print(f"\n📊 Excel文件已生成: {excel_file}")
else:
    print("\n⚠️ 未生成Excel文件: 无有效数据")