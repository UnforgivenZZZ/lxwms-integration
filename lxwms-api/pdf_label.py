import pdfplumber
import re

def extract_tracking_numbers(pdf_path):
    tracking_numbers = []
    pattern = r'USPS TRACKING #\s+(9400\s\d{4}\s\d{4}\s\d{4}\s\d{4}\s\d{2})'
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                # 处理换行符和多空格
                normalized_text = re.sub(r'\s+', ' ', text)
                matches = re.findall(pattern, normalized_text)
                tracking_numbers.extend(matches)
                print(matches)
    
    return tracking_numbers

# 使用示例
tracking_list = extract_tracking_numbers('./sorted_output.pdf')
print(f"Found {len(tracking_list)} tracking numbers:")
dups = set()
for tn in tracking_list:
    if tn in dups:
        print(tn)
    dups.add(tn)
