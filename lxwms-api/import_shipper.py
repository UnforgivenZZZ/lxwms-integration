import argparse
import pandas as pd


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="check if there is new inbound order")
        # Define the command-line arguments
    parser.add_argument('--wave', required=True, help="name of customer: ie: ")
    args = parser.parse_args()
    data = []
    with open(f"{args.wave}_po.txt",'r') as f:
        for po in f:
            
            row = {
                    "工作号\n#JOBNUM": po,
                    "发件人代码                      #SFCODE": "AID-268"
                }
            data.append(row)
        df = pd.DataFrame(data)

    # 写入Excel文件
    try:
        df.to_excel(
            f"{args.wave}_shipper.xlsx",
            index=False,
            engine='openpyxl',
            columns=["工作号\n#JOBNUM", "发件人代码                      #SFCODE"]
        )
        print(f"\nExcel文件已成功生成：{args.wave}_shipper.xlsx")
    except Exception as e:
        print(f"写入Excel文件时出错: {str(e)}")
