import os
import re
import pdfplumber
from PyPDF2 import PdfReader, PdfWriter

def extract_skus(page):
    """从PDF页面底部提取SKU及数量（支持单SKU和多SKU格式）"""
    # 提取页面底部文本（假设SKU信息在页面最后5行）
    text = "\n".join(page.extract_text().split('\n')[-5:])
    
    # 统一清理文本中的多余空格和特殊符号
    text = re.sub(r'\s+', ' ', text).strip()
    
    # 正则表达式匹配两种SKU格式
    sku_pattern = re.compile(
        r'(X[\dA-Z]+)'      # 匹配X开头的SKU编码
        r'[\s*]*x?[\s*]*'   # 匹配分隔符（支持 x、* 或空格）
        r'(\d+)'            # 匹配数量
    )
    
    # 分号分隔的多SKU处理（忽略末尾的 *1）
    sku_items = []
    for segment in text.split(';'):
        segment = segment.strip()
        if segment.startswith('*'):
            continue  # 忽略 *1 结尾
        
        match = sku_pattern.search(segment)
        if match:
            sku, qty = match.groups()
            sku_items.append((sku, int(qty)))
    sku_items.sort()
    return sku_items

def sort_key(item):
    """
    自定义排序规则：
    1. 单SKU页面优先，按字母顺序排序
    2. 多SKU页面排最后，保持原顺序
    """
    skus, _, _ = item
    if len(skus) == 1:
        # 单SKU：使用自然排序
        return (0, natural_sort_key(skus[0]))
    else:
        # 多SKU：统一放到最后
        return (1, float('inf'))  # 使用inf保证多SKU始终在最后

def natural_sort_key(s):
    """增强自然排序：处理字母数字混合"""
    return [int(c) if c.isdigit() else c.lower() 
            for c in re.split(r'(\d+)', s)]

def sort_and_merge_pdfs(input_paths, output_path):
    """精确排序合并PDF"""
    # 收集所有页面信息
    all_pages = []
    
    for filepath in input_paths:
        try:
            with pdfplumber.open(filepath) as pdf:
                reader = PdfReader(filepath)
                for page_num in range(len(reader.pages)):
                    try:
                        page = pdf.pages[page_num]
                        skus = extract_skus(page)
                        if not skus:
                            print(f"警告：{os.path.basename(filepath)} 第{page_num+1}页无SKU，已跳过")
                            continue
                        print(f"{os.path.basename(filepath)} 第{page_num+1}, {skus}")
                        all_pages.append((
                            len(skus),
                            skus,
                            filepath,
                            page_num
                        ))
                    except Exception as e:
                        print(f"文件 {os.path.basename(filepath)} 第{page_num+1}页 读取失败：{str(e)}")
                        continue
        except Exception as e:
            print(f"文件 {os.path.basename(filepath)} 读取失败：{str(e)}")
            continue

    if not all_pages:
        raise ValueError("没有可处理的页面")

    # 执行排序
    all_pages.sort()
    
    # 合并页面
    writer = PdfWriter()
    cached_readers = {}
    sku_set = set()
    for _, skus, src_file, src_page in all_pages:
        print(skus)
        if src_file not in cached_readers:
            cached_readers[src_file] = PdfReader(src_file)
        
        reader = cached_readers[src_file]
        writer.add_page(reader.pages[src_page])
    
    # 写入最终文件
    with open(output_path, "wb") as f:
        writer.write(f)
    
    # 清理资源
    for reader in cached_readers.values():
        if hasattr(reader, 'stream'):
            reader.stream.close()

def get_pdf_files(directory):
    """安全获取PDF文件列表"""
    return [os.path.join(root, f) 
            for root, _, files in os.walk(directory) 
            for f in files if f.lower().endswith('.pdf')]

# 使用示例
if __name__ == "__main__":
    folder = input('wave: ')
    input_dir = f"./downloads/{folder}"
    output_file = f"sorted_{folder}.pdf"
    
    pdf_files = get_pdf_files(input_dir)
    
    if not pdf_files:
        print("错误：目录中没有PDF文件")
        exit(1)
        
    try:
        sort_and_merge_pdfs(pdf_files, output_file)
        print(f"成功生成排序文件：{output_file}")
        print("排序规则：")
        print("1. 单SKU页面按字母数字顺序排列")
        print("2. 多SKU页面统一放在文件末尾")
    except Exception as e:
        print(f"处理失败：{str(e)}")