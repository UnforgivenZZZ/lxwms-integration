import json
import base64
import re
import csv
from openpyxl import Workbook

import io
from PyPDF2 import PdfMerger, PdfReader

def process_file(input_file, wave):
    # List to store all PDF pages with their sort keys
    all_pages = []
    orders_info = []

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Extract order number and JSON string
            parts = re.split(r',(?={)', line, 1)
            if len(parts) < 2:
                continue
                
            order_number, json_str = parts
            
            try:
                # Parse JSON
                data = json.loads(json_str)
                shipment = data.get('shipment', {})
                tracking_number = shipment['trackings'][0]['tracking_number']
                courier_service = shipment.get('courier_service', {})
                shipping_service = 'USPS'
                
                # Add to orders info for Excel
                orders_info.append({
                    'order_number': order_number,
                    'tracking_number': tracking_number,
                    'shipping_service': shipping_service
                })

                
                # Extract all SKUs
                skus = data['skus']
                sorted_skus = sorted(skus)
                sort_key = (len(sorted_skus), ';'.join(sorted_skus))
                
                # Process shipping documents
                docs = shipment.get('shipping_documents', [])
                for doc in docs:
                    for base64_str in doc.get('base64_encoded_strings', []):
                        pdf_data = base64.b64decode(base64_str)
                        all_pages.append((sort_key, pdf_data))
                    break
                            
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error processing {order_number}: {str(e)}")
                raise e
    
    # Sort pages by SKU criteria
    all_pages.sort(key=lambda x: x[0])
    
    # Merge all PDF pages into one file
    merger = PdfMerger()
    for _, pdf_data in all_pages:
        pdf_stream = io.BytesIO(pdf_data)
        merger.append(PdfReader(pdf_stream))
    
    # Write the combined PDF
    output_filename = f"sorted_{wave}.pdf"
    with open(output_filename, 'wb') as output_file:
        merger.write(output_file)
    
    # Write Excel file
   # Create Excel workbook
    excel_filename = f"{wave}_orders.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Orders"
    
    # Write headers
    headers = ['Outbound Order Num/出库单号', 'Tracking Number/物流跟踪号', 'Shipping service/承运商']
    ws.append(headers)
    
    # Write order data
    for order in orders_info:
        ws.append([
            order['order_number'],
            order['tracking_number'],
            order['shipping_service']
        ])
    
    # Save Excel file
    wb.save(excel_filename)
    
    print(f"Created combined PDF: {output_filename}")
    print(f"Created orders Excel: {excel_filename}")
if __name__ == "__main__":
    wave = input("Enter wave name: ")
    input_filename = f"{wave}.txt"
    process_file(input_filename, wave)