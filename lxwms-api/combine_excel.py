import pandas as pd
import os

def combine_excel_files():
    # 提示用户输入文件路径
    file_paths = []
    print("请输入Excel文件路径（输入-1结束输入）:")
    
    while True:
        path = input("> ").strip()  # 去除首尾空格
        if path == "-1":
            break
        if not os.path.exists(path):
            print(f"文件不存在: {path}")
            continue
        if not path.endswith('.xlsx'):
            print(f"仅支持.xlsx文件: {path}")
            continue
        file_paths.append(path)
        print(f"已添加: {path}")

    # 检查是否输入了有效文件
    if not file_paths:
        print("未输入有效文件！")
        return

    # 合并所有Excel文件
    try:
        # 读取所有文件
        dfs = []
        for file in file_paths:
            df = pd.read_excel(file)
            dfs.append(df)
            print(f"已读取: {os.path.basename(file)}")

        # 合并数据
        combined_df = pd.concat(dfs, ignore_index=True)
        
        # 保存合并结果
        output_name = input("请输入输出文件名（例如 combined.xlsx）: ").strip()
        if not output_name.endswith('.xlsx'):
            output_name += '.xlsx'
            
        combined_df.to_excel(output_name, index=False)
        print(f"\n合并完成！结果已保存为: {output_name}")
        print(f"总行数: {len(combined_df)}")

    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    combine_excel_files()